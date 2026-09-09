#!/usr/bin/env python3
"""One-time import of contest recap datasets into the PostgreSQL serving layer.

    import_recaps.py --contest-dir /var/tmp/contests          # import every recap in recaps.yaml
    import_recaps.py --contest-dir /var/tmp/contests --dry-run

WHY THIS IS A ONE-TIME IMPORT AND NOT A REFRESH JOB.

Contest recaps are static. ARRL DX CW and SSB ran in March 2026; the contests are over, the
signatures are frozen, and no amount of re-reading will change a number. There is nothing to
keep fresh — so this is not part of refresh.py's cadence groups. It runs once per contest,
when that contest's dataset is built, and never again.

WHY IT READS SQLITE RATHER THAN REBUILDING FROM CLICKHOUSE.

The datasets are built from ClickHouse by ionis-devel/contests/export_contest_sqlite.py, so
rebuilding looks tempting. It is not safe: that script's current PSKR query hardcodes
avg_distance = 0, while the published recap pages show real distances (160m: 3,476 km). The
files on disk do not match what the current script would produce, and reproducing them means
resolving that provenance question first. Importing the artifact that actually rendered the
published pages has no such risk.

WHAT THIS ENDS.

publish.py read 1.3 GB of SQLite at render time, off a filesystem that existed only on the
9975. That coupling is what broke the contest pages when publishing moved to publish-1 — the
loader warned, returned None, and the run still reported "2 recap(s) loaded" and exited 0.
After this import nothing reads SQLite at render time, on any host.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sqlite3
import sys
from pathlib import Path

import psycopg
import yaml

ROOT = Path(os.environ.get("HAMSTATS_ROOT") or Path(__file__).parent)
DB_FILE = os.environ.get("HAMSTATS_DB_FILE", "/etc/hamstats/db-rw.dsn")

sys.path.insert(0, str(ROOT))
from publish import load_recap_data_sqlite  # noqa: E402

# Static data does not expire. The serving layer's staleness check compares refreshed_at
# against max_age, and a recap that is a year old is exactly as correct as one imported today.
STATIC = "100 years"

DATASETS = ("band_summary", "hourly_activity", "solar_timeline", "distance_stats")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--contest-dir", required=True,
                    help="directory holding the recap .sqlite files")
    ap.add_argument("--dry-run", action="store_true", help="read and report, write nothing")
    args = ap.parse_args()

    os.environ["CONTEST_DATA_DIR"] = args.contest_dir
    import publish
    publish.CONTEST_DATA_DIR = Path(args.contest_dir)

    recaps = yaml.safe_load((ROOT / "data" / "recaps.yaml").read_text()) or []
    print(f"Importing {len(recaps)} recap(s) from {args.contest_dir}")

    staged, missing = [], []
    for recap in recaps:
        slug = recap.get("slug")
        # load_recap_data is publish.py's OWN loader, unchanged. Whatever it produced when
        # rendering from SQLite is exactly what lands in PostgreSQL — the import cannot drift
        # from the thing it is replacing, because it is the same code.
        data = load_recap_data_sqlite(recap)
        if data is None:
            print(f"  MISSING  {slug}: no dataset at {args.contest_dir}/{recap.get('dataset')}")
            missing.append(slug)
            continue
        for key in DATASETS:
            rows = data.get(key) or []
            staged.append((f"recap:{slug}:{key}", rows))
            print(f"  {slug:22} {key:18} {len(rows):>5} rows")

    if missing:
        # Importing a partial set would leave some recaps rendering empty with no indication
        # that anything is wrong -- the exact failure this import exists to end.
        print(f"ERROR: {len(missing)} recap(s) had no dataset: {', '.join(missing)}. "
              f"Nothing written.", file=sys.stderr)
        return 1

    if args.dry_run:
        print("Dry run — nothing written.")
        return 0

    dsn = Path(DB_FILE).read_text().strip()
    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute((ROOT / "sql" / "serving_schema.sql").read_text())
        for name, rows in staged:
            conn.execute(
                """
                INSERT INTO serving.query_results
                    (name, payload, row_count, refreshed_at, max_age,
                     source_rows_read, source_elapsed_ms)
                VALUES (%s, %s::jsonb, %s, now(), %s::interval, NULL, NULL)
                ON CONFLICT (name) DO UPDATE SET
                    payload      = EXCLUDED.payload,
                    row_count    = EXCLUDED.row_count,
                    refreshed_at = EXCLUDED.refreshed_at,
                    max_age      = EXCLUDED.max_age
                """,
                (name, json.dumps(rows, default=_json_default), len(rows), STATIC),
            )
        conn.commit()
    print(f"Wrote {len(staged)} recap dataset(s) to the serving layer.")
    return 0


def _json_default(o):
    if isinstance(o, (dt.datetime, dt.date)):
        return o.isoformat()
    raise TypeError(f"{type(o).__name__} is not JSON-serialisable: {o!r}")


if __name__ == "__main__":
    sys.exit(main())
