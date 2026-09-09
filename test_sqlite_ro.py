#!/usr/bin/env python3
"""Checks that contest datasets open without needing write access.

    python3 test_sqlite_ro.py

Stdlib only. Loads the real helper out of publish.py rather than copying it — publish.py
imports clickhouse_connect at module scope, so it cannot simply be imported here.

WHY THIS EXISTS. The ARRL-DX datasets are WAL-mode SQLite in a directory the publish
service does not own. A WAL database needs to create a `-shm` sidecar even to READ, so
every run logged "attempt to write a readonly database" and dropped both contest recaps.
"""
import os
import sqlite3
import stat
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).with_name("publish.py").read_text()
_start = SRC.index("def sqlite_ro_uri")
_end = SRC.index("def load_recap_data")
_ns = {"Path": Path}
exec("from urllib.parse import quote\n" + SRC[_start:_end], _ns)  # noqa: S102
sqlite_ro_uri = _ns["sqlite_ro_uri"]

failures = []


def check(label, got, want):
    if got == want:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}: got {got!r}, want {want!r}")
        failures.append(label)


def make_wal_db(path):
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE TABLE pskr_signatures (band TEXT, spot_count INT)")
    conn.execute("INSERT INTO pskr_signatures VALUES ('20m', 7)")
    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    conn.close()
    for side in ("-wal", "-shm"):
        Path(str(path) + side).unlink(missing_ok=True)


with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp) / "contests"
    d.mkdir()
    db = d / "arrl-dx-cw-2026.sqlite"
    make_wal_db(db)
    check("fixture really is WAL", db.read_bytes()[18], 2)

    # the directory the service sees: readable, not writable
    os.chmod(d, stat.S_IRUSR | stat.S_IXUSR)

    print("== the bug, reproduced ==")
    try:
        sqlite3.connect(str(db)).execute("SELECT * FROM pskr_signatures").fetchall()
        check("a plain connect fails on a WAL db in a read-only dir", "no error", "readonly error")
    except sqlite3.OperationalError as e:
        check("a plain connect fails on a WAL db in a read-only dir",
              "readonly" in str(e), True)

    print("== the fix ==")
    rows = sqlite3.connect(sqlite_ro_uri(db), uri=True).execute(
        "SELECT band, spot_count FROM pskr_signatures").fetchall()
    check("the read-only URI returns the rows", rows, [("20m", 7)])

    print("== and it stays read-only ==")
    conn = sqlite3.connect(sqlite_ro_uri(db), uri=True)
    try:
        conn.execute("INSERT INTO pskr_signatures VALUES ('40m', 1)")
        check("a write through the read-only handle is refused", "no error", "refused")
    except sqlite3.OperationalError as e:
        check("a write through the read-only handle is refused",
              "readonly" in str(e), True)
    conn.close()
    check("no sidecar files were created", sorted(p.name for p in d.iterdir()), [db.name])

    print("== immutable is only claimed when there is no WAL to ignore ==")
    check("no -wal present -> immutable", "immutable=1" in sqlite_ro_uri(db), True)
    os.chmod(d, 0o700)
    Path(str(db) + "-wal").write_bytes(b"")
    # a pending WAL must NOT be skipped: immutable would read back silently stale
    check("-wal present -> NOT immutable", "immutable" in sqlite_ro_uri(db), False)
    check("-wal present -> still read-only", "mode=ro" in sqlite_ro_uri(db), True)

print()
print("== against the real datasets on this host ==")
real = Path(os.environ.get("CONTEST_DATA_DIR", "/mnt/sourceforge/contests"))
for name in ("arrl-dx-cw-2026.sqlite", "arrl-dx-ssb-2026.sqlite"):
    p = real / name
    if not p.exists():
        print(f"  SKIP  {name} not present")
        continue
    n = sqlite3.connect(sqlite_ro_uri(p), uri=True).execute(
        "SELECT COUNT(*) FROM pskr_signatures").fetchone()[0]
    check(f"{name} reads back rows", n > 0, True)

print()
if failures:
    print(f"  {len(failures)} FAILED")
    sys.exit(1)
print("  all checks passed")
