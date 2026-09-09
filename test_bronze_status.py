#!/usr/bin/env python3
"""Checks for the bronze-status freshness labels.

    python3 test_bronze_status.py

Stdlib only, and it loads the real functions out of publish.py rather than copying them —
publish.py imports clickhouse_connect at module scope, so it cannot simply be imported here,
and a copied predicate would drift from the code it claims to check.

WHY THIS EXISTS. The status column used one global threshold: 1 day = Current, more = behind.
RBN publishes each day's archive the following day and we fetch at 16:00 UTC, so every
morning a perfectly healthy RBN read "2 days behind", flipped to "Current" after the fetch,
and flipped back at midnight. The label was measuring against today's date instead of against
what each source can actually deliver.
"""
import datetime as dt
import sys
from pathlib import Path

SRC = Path(__file__).with_name("publish.py").read_text()
_start = SRC.index("# How stale each source can legitimately be")
_end = SRC.index("def build_context")
_ns = {"dt": dt}
exec(SRC[_start:_end], _ns)          # noqa: S102 - loading the real implementation
enrich_bronze_status = _ns["enrich_bronze_status"]
expected_lag_days = _ns["expected_lag_days"]

TODAY = dt.date(2026, 9, 9)
BEFORE_FETCH = dt.datetime(2026, 9, 9, 8, 16)    # rbn-download runs 16:00 UTC
AFTER_FETCH = dt.datetime(2026, 9, 9, 17, 5)     # +ingest 16:30, +margin

failures = []


def check(label, got, want):
    if got == want:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}: got {got!r}, want {want!r}")
        failures.append(label)


def status_for(name, latest, now):
    data = {"bronze_status": [{"source_name": name, "latest_date": latest}]}
    enrich_bronze_status(data, now)
    return data["bronze_status"][0]["status"]


print("== the reported table, before RBN's daily fetch ==")
check("WSPR at T-1 is Current", status_for("WSPR", dt.date(2026, 9, 8), BEFORE_FETCH), "Current")
# the bug: this said "2 days behind" every morning
check("RBN at T-2 is Current before the fetch",
      status_for("RBN", dt.date(2026, 9, 7), BEFORE_FETCH), "Current")
check("PSK Reporter same-day is Live",
      status_for("PSK Reporter", dt.date(2026, 9, 9), BEFORE_FETCH), "Live")
check("Solar same-day is Live", status_for("Solar", dt.date(2026, 9, 9), BEFORE_FETCH), "Live")
check("Contest is Static", status_for("Contest", None, BEFORE_FETCH), "Static")

print("== after the fetch window, the expectation tightens ==")
# the check that must NOT be lost: a missed fetch is still reported
check("RBN still at T-2 after the fetch is 1 day behind",
      status_for("RBN", dt.date(2026, 9, 7), AFTER_FETCH), "1 day behind")
check("RBN at T-1 after the fetch is Current",
      status_for("RBN", dt.date(2026, 9, 8), AFTER_FETCH), "Current")

print("== genuine lateness, reported relative to the expectation ==")
check("RBN three days old is 2 days behind",
      status_for("RBN", dt.date(2026, 9, 6), AFTER_FETCH), "2 days behind")
check("WSPR four days old is 3 days behind",
      status_for("WSPR", dt.date(2026, 9, 5), AFTER_FETCH), "3 days behind")
check("a live source two days stale is 2 days behind",
      status_for("Solar", dt.date(2026, 9, 7), AFTER_FETCH), "2 days behind")
check("singular day, not days", status_for("Solar", dt.date(2026, 9, 8), AFTER_FETCH), "1 day behind")

print("== degenerate inputs still handled ==")
check("no date at all", status_for("WSPR", None, BEFORE_FETCH), "—")
check("unparseable date", status_for("WSPR", "not-a-date", BEFORE_FETCH), "—")
check("future date is Live", status_for("WSPR", dt.date(2026, 9, 10), BEFORE_FETCH), "Live")

print("== expectations themselves ==")
check("RBN expects 2 before the fetch", expected_lag_days("RBN", BEFORE_FETCH), 2)
check("RBN expects 1 after the fetch", expected_lag_days("RBN", AFTER_FETCH), 1)
check("an unknown source keeps the old default of 1",
      expected_lag_days("Something New", BEFORE_FETCH), 1)

print()
if failures:
    print(f"  {len(failures)} FAILED")
    sys.exit(1)
print("  all checks passed")
