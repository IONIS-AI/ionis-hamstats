#!/usr/bin/env python3
"""Materialise ClickHouse aggregates into the PostgreSQL serving layer.

    refresh.py --group live      # hourly
    refresh.py --group daily
    refresh.py --group weekly
    refresh.py --group all --dry-run

publish.py used to run all 24 queries against ClickHouse on every 3-hourly run: 123,962,343,315
rows read to publish 4,398 of them, roughly a trillion rows a day. ClickHouse stays the source of
truth and the only place the raw data lives; this moves the *reading* of already-aggregated
results onto Postgres, at a cadence matched to how fast each result actually changes.

The DSN comes from a file rendered by Vault Agent (HAMSTATS_DB_FILE), the same indirection IBX
uses -- no credential in this file, in the environment, or in the unit.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

import clickhouse_connect
import psycopg
import yaml

# Packaged artifacts (see publish.py). Defaults to this file's directory so a clone works.
ROOT = Path(os.environ.get("HAMSTATS_ROOT") or Path(__file__).parent)
QUERIES_DIR = ROOT / "queries"
CADENCE = QUERIES_DIR / "cadence.yml"
SCHEMA = ROOT / "sql" / "serving_schema.sql"

# LAN address, not the DAC. This defaulted to 10.60.1.1, the Thunderbolt point-to-point link
# between the 9975 and the M3 — correct only from those two machines. From publish-1 it is
# unroutable, and the failure is a 10-second connect timeout per query rather than anything
# that names the cause. publish.py has always defaulted to the LAN address; this did not.
#
# Override with CH_HOST for a host that is actually on the DAC, where it is much faster.
CH_HOST = os.environ.get("CH_HOST", "192.168.1.90")
CH_PORT = int(os.environ.get("CH_PORT", "8123"))
DB_FILE = os.environ.get("HAMSTATS_DB_FILE", "/etc/hamstats/db.dsn")


class JSONEncoder(json.JSONEncoder):
    """Dates and datetimes become ISO strings; everything else must already be JSON-safe.

    ClickHouse hands back dt.date / dt.datetime for Date and DateTime columns. Templates never
    call date methods on query results -- only on calendar and recap data, which does not come
    through here -- and enrich_bronze_status parses ISO strings, so ISO is a faithful
    representation on the consuming side. Anything this cannot encode raises rather than being
    coerced: an unexpected type reaching the payload silently is how a shape change becomes a
    wrong page instead of an error.
    """

    def default(self, o):
        if isinstance(o, (dt.datetime, dt.date)):
            return o.isoformat()
        raise TypeError(f"{type(o).__name__} is not JSON-serialisable: {o!r}")


def load_groups() -> dict:
    return yaml.safe_load(CADENCE.read_text())["groups"]


def run_query(client, name: str) -> tuple[list[dict], int, int]:
    """Run one query. Returns (rows, rows_read, elapsed_ms).

    Mirrors publish.py's own row normalisation so the payload is byte-identical to what
    publish.py used to build for itself -- same null-byte stripping, same float rounding.
    """
    sql = (QUERIES_DIR / f"{name}.sql").read_text()
    result = client.query(sql)
    columns = result.column_names
    rows = []
    for row in result.result_rows:
        d = {}
        for i, col in enumerate(columns):
            v = row[i]
            if isinstance(v, bytes):
                v = v.decode("utf-8", errors="replace").rstrip("\x00").strip()
            elif isinstance(v, str):
                v = v.rstrip("\x00").strip()
            elif isinstance(v, float):
                # NON-FINITE FLOATS BECOME null. ClickHouse reports a missing aggregate as JSON
                # null -- storm_snr_comparison.after_snr is null for a storm too recent to have
                # an "after" -- but clickhouse_connect hands it to Python as float('nan').
                # json.dumps then emits a bare NaN, a non-standard extension PostgreSQL rejects:
                #
                #     invalid input syntax for type json, Token "NaN" is invalid
                #
                # null is what the source says and what the templates already handle. Infinity
                # gets the same treatment for the same reason.
                v = None if (v != v or v in (float("inf"), float("-inf"))) else round(v, 2)
            d[col] = v
        rows.append(d)
    summary = getattr(result, "summary", None) or {}
    return rows, int(summary.get("read_rows", 0) or 0), int(float(summary.get("elapsed_ns", 0) or 0) / 1e6)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--group", required=True, help="live | daily | weekly | all")
    ap.add_argument("--dry-run", action="store_true", help="query ClickHouse, write nothing")
    args = ap.parse_args()

    groups = load_groups()
    if args.group == "all":
        selected = [(g, spec) for g, spec in groups.items()]
    elif args.group in groups:
        selected = [(args.group, groups[args.group])]
    else:
        sys.exit(f"unknown group {args.group!r}; have: {', '.join(groups)} (or 'all')")

    print(f"Refresh — {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC, group(s): "
          f"{', '.join(g for g, _ in selected)}")

    ch = clickhouse_connect.get_client(host=CH_HOST, port=CH_PORT)

    results, failures = [], []
    total_read = 0
    for group, spec in selected:
        for name in spec["queries"]:
            try:
                rows, read, elapsed = run_query(ch, name)
            except Exception as e:
                # DO NOT WRITE ANYTHING FOR A FAILED QUERY. publish.py's old behaviour was to
                # catch this, set data[name] = [] and carry on, so a ClickHouse problem rendered
                # as a page with empty tables and a successful exit. Leaving the previous row in
                # place means the site serves the last good numbers and the staleness check
                # surfaces the outage, instead of the outage looking like "no data exists".
                print(f"  FAILED  {name}: {e}", file=sys.stderr)
                failures.append(name)
                continue
            total_read += read
            results.append((name, rows, read, elapsed, spec["max_age"]))
            print(f"  {name:26} {len(rows):>6} row(s)  read {read:>15,}  {elapsed:>6} ms")

    print(f"  {total_read:,} rows read from ClickHouse for {sum(len(r[1]) for r in results)} published rows")

    if args.dry_run:
        print("Dry run — nothing written.")
        return 1 if failures else 0

    dsn = Path(DB_FILE).read_text().strip()
    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(SCHEMA.read_text())
        for name, rows, read, elapsed, max_age in results:
            conn.execute(
                """
                INSERT INTO serving.query_results
                    (name, payload, row_count, refreshed_at, max_age,
                     source_rows_read, source_elapsed_ms)
                VALUES (%s, %s::jsonb, %s, now(), %s::interval, %s, %s)
                ON CONFLICT (name) DO UPDATE SET
                    payload           = EXCLUDED.payload,
                    row_count         = EXCLUDED.row_count,
                    refreshed_at      = EXCLUDED.refreshed_at,
                    max_age           = EXCLUDED.max_age,
                    source_rows_read  = EXCLUDED.source_rows_read,
                    source_elapsed_ms = EXCLUDED.source_elapsed_ms
                """,
                (name, json.dumps(rows, cls=JSONEncoder), len(rows), max_age, read, elapsed),
            )
        conn.commit()
    print(f"Wrote {len(results)} result set(s) to the serving layer.")

    if failures:
        # Non-zero so the timer's unit lands in `failed`. The previous rows are intact and the
        # site keeps serving them; what must not happen is this passing quietly.
        print(f"ERROR: {len(failures)} quer(y/ies) failed and were NOT written, leaving the "
              f"previous results in place: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
