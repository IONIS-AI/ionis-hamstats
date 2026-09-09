#!/usr/bin/env python3
"""Checks for the PostgreSQL serving layer.

    python3 test_serving.py

Stdlib + pyyaml only; needs neither ClickHouse nor PostgreSQL.

WHY THIS EXISTS. publish.py stops querying ClickHouse and reads materialised results out of
Postgres instead. The results travel as JSONB, so every value makes a round trip through JSON --
and ClickHouse hands back dt.date / dt.datetime objects for Date and DateTime columns. If that
round trip changes what a template renders, the site changes silently and nothing fails.
"""
import datetime as dt
import json
import sys
import types
from pathlib import Path

sys.modules.setdefault("clickhouse_connect", types.ModuleType("clickhouse_connect"))
sys.path.insert(0, str(Path(__file__).parent))
import publish   # noqa: E402
import yaml      # noqa: E402

SRC = Path("refresh.py").read_text()
_ns = {"dt": dt, "json": json}
_start = SRC.index("class JSONEncoder")
_end = SRC.index("def load_groups")
exec(SRC[_start:_end], _ns)          # noqa: S102 - the real encoder, not a copy
JSONEncoder = _ns["JSONEncoder"]

failures = []


def check(label, got, want):
    if got == want:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}: got {got!r}, want {want!r}")
        failures.append(label)


def roundtrip(obj):
    return json.loads(json.dumps(obj, cls=JSONEncoder))


print("== every query is scheduled, and nothing is scheduled that does not exist ==")
# A query added to queries/ but not to cadence.yml would never be refreshed. publish would
# report it missing rather than serving a stale value -- but only after it reached production.
groups = yaml.safe_load(Path("queries/cadence.yml").read_text())["groups"]
declared = [q for g in groups.values() for q in g["queries"]]
on_disk = {p.stem for p in Path("queries").glob("*.sql")}
check("no query is left unscheduled", sorted(on_disk - set(declared)), [])
check("no schedule names a missing query", sorted(set(declared) - on_disk), [])
check("no query is scheduled twice", len(declared), len(set(declared)))
check("every group declares an interval and a max_age",
      all("interval" in g and "max_age" in g for g in groups.values()), True)

print("== dates survive the round trip as far as the consumer is concerned ==")
# bronze_status.latest_date is the one ClickHouse date a template's output depends on.
NOW = dt.datetime(2026, 9, 9, 8, 0)
def status_with(latest):
    d = {"bronze_status": [{"source_name": "WSPR", "latest_date": latest}]}
    publish.enrich_bronze_status(d, NOW)
    return d["bronze_status"][0]["status"], d["bronze_status"][0]["latest_display"]

as_date = status_with(dt.date(2026, 9, 8))
as_json = status_with(roundtrip({"d": dt.date(2026, 9, 8)})["d"])
check("a date object and its JSON form render identically", as_json, as_date)
check("and that is the correct answer, not two matching wrongs", as_date, ("Current", "2026-09-08"))

dtm = dt.datetime(2026, 9, 8, 20, 0, 0)
check("datetimes round-trip to ISO", roundtrip({"t": dtm})["t"], "2026-09-08T20:00:00")
check("a datetime still classifies", status_with(roundtrip({"t": dtm})["t"])[0], "Current")

print("== ordinary values are unchanged ==")
payload = [{"band": "20m", "count": 1234567, "snr": -12.34, "ratio": 0.5,
            "name": None, "flag": True, "nested": {"a": [1, 2, 3]}}]
check("a representative row survives exactly", roundtrip(payload), payload)
check("large integers keep precision", roundtrip({"n": 37848290025})["n"], 37848290025)

print("== an unexpected type is an error, not a coercion ==")
# Silently str()-ing an unknown object is how a ClickHouse type change becomes a wrong page
# instead of a failed run.
class Weird:
    def __repr__(self): return "<weird>"
try:
    json.dumps({"x": Weird()}, cls=JSONEncoder)
    check("unknown types raise", "no error", "TypeError")
except TypeError as e:
    check("unknown types raise", "not JSON-serialisable" in str(e), True)

print("== publish reports missing and stale results ==")
code = "\n".join(l for l in Path("publish.py").read_text().splitlines()
                 if not l.lstrip().startswith("#"))
check("publish no longer runs the queries by default",
      "data, stale = load_from_serving()" in code, True)
check("the ClickHouse path is still reachable for comparison",
      "--from-clickhouse" in code, True)
check("stale results cause a non-zero exit", "if stale:" in code and "return 1" in code, True)
check("a missing result is reported, not silently empty",
      "has never been refreshed" in Path("publish.py").read_text(), True)

print("== a failed query must not overwrite a good result ==")
rcode = Path("refresh.py").read_text()
check("refresh skips failed queries rather than writing []",
      "failures.append(name)" in rcode and "continue" in rcode, True)
check("and exits non-zero so the timer shows it", "return 1" in rcode, True)
check("the schema forbids a row_count that disagrees with the payload",
      "row_count = jsonb_array_length(payload)" in Path("sql/serving_schema.sql").read_text(), True)

print()
if failures:
    print(f"  {len(failures)} FAILED")
    sys.exit(1)
print("  all checks passed")
