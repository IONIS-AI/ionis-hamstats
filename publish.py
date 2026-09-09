#!/usr/bin/env python3
"""Ham Stats publish pipeline.

Queries ClickHouse, renders Jinja2 templates, optionally commits and pushes.

Usage:
    python publish.py              # render only (preview)
    python publish.py --push       # render + commit + push
    python publish.py --build      # render + mkdocs build (local preview)
    python publish.py --dry-run    # list what would change
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import quote

import clickhouse_connect
import yaml
from jinja2 import Environment, FileSystemLoader, Undefined

import contest_calendar

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# TWO ROOTS, BECAUSE AN RPM SPLITS THEM.
#
# ROOT is where the versioned artifacts live -- queries, templates, SQL, static data. Installed
# to /usr/share/ionis-hamstats and owned by the package, so what runs in production is the
# reviewed and built copy rather than whatever happens to be in a working tree.
#
# CONTENT_DIR is the git checkout the rendered pages are written into and pushed from. That has
# to stay a working tree because publishing IS a commit to it.
#
# Both default to this file's own directory, so running publish.py straight out of a clone
# behaves exactly as before.
ROOT = Path(os.environ.get("HAMSTATS_ROOT") or Path(__file__).parent)
CONTENT_DIR = Path(os.environ.get("HAMSTATS_CONTENT_DIR") or ROOT)
QUERIES_DIR = ROOT / "queries"
TEMPLATES_DIR = ROOT / "templates"
DOCS_DIR = CONTENT_DIR / "docs"

# Files never overwritten by templates
STATIC_PATHS = frozenset({
    "about.md",
    "methodology/index.md",
    "methodology/signatures.md",
    "methodology/data-quality.md",
    "CNAME",
    "bands/CNAME",
})

# Band metadata — low freq → high freq (site navigation order)
BANDS = [
    {"name": "160m", "freq_mhz": "1.8",  "adif": 102,
     "desc": "Top Band — nighttime DX, noise-limited"},
    {"name": "80m",  "freq_mhz": "3.5",  "adif": 103,
     "desc": "Nighttime domestic — reliable regional propagation"},
    {"name": "60m",  "freq_mhz": "5.3",  "adif": 104,
     "desc": "Channelized band — limited allocations, NVIS propagation studies"},
    {"name": "40m",  "freq_mhz": "7.0",  "adif": 105,
     "desc": "The workhorse — day and night, domestic and DX"},
    {"name": "30m",  "freq_mhz": "10.1", "adif": 106,
     "desc": "CW/digital only — quiet band, excellent propagation studies"},
    {"name": "20m",  "freq_mhz": "14.0", "adif": 107,
     "desc": "The DX band — daytime worldwide, first band to open with solar activity"},
    {"name": "17m",  "freq_mhz": "18.1", "adif": 108,
     "desc": "WARC band — no contests, quieter activity, good DX indicator"},
    {"name": "15m",  "freq_mhz": "21.0", "adif": 109,
     "desc": "Daytime DX — needs moderate solar activity to open"},
    {"name": "12m",  "freq_mhz": "24.9", "adif": 110,
     "desc": "WARC band — sporadic openings, solar-sensitive"},
    {"name": "10m",  "freq_mhz": "28.0", "adif": 111,
     "desc": "Highest HF band — wide open at solar max, dead at solar min"},
]

ADIF_TO_BAND = {b["adif"]: b["name"] for b in BANDS}
BAND_TO_ADIF = {b["name"]: b["adif"] for b in BANDS}

# Contest SQLite datasets (on 9975WX)
CONTEST_DATA_DIR = Path(os.environ.get(
    "CONTEST_DATA_DIR", "/mnt/sourceforge/contests",
))

# IONIS prediction: KI7MT (DN13) → representative contest destinations
TX_GRID = "DN13"
PREDICTION_DESTINATIONS = [
    {"label": "Europe (JN48)",    "grid": "JN48"},
    {"label": "Japan (PM95)",     "grid": "PM95"},
    {"label": "S. America (GG87)", "grid": "GG87"},
    {"label": "Africa (KG33)",    "grid": "KG33"},
    {"label": "Oceania (QF56)",   "grid": "QF56"},
    {"label": "Caribbean (FK68)", "grid": "FK68"},
]
PREDICTION_BANDS = ["10m", "12m", "15m", "17m", "20m", "30m", "40m", "60m", "80m", "160m"]

# Sigma-to-dB conversion (WSPR 20m reference — within 1 dB of all bands)
WSPR_MEAN_DB = -17.53
WSPR_STD_DB = 6.7

# Paths to IONIS model components (V22-gamma + PhysicsOverrideLayer)
# The model, its config and its weights are package data inside ionis-validate, and
# load_model() finds them itself. There used to be four constants here pointing at
# /mnt/ai-stack/ionis-ai/ionis-training/versions/{common,v22}/ — a directory that does not
# exist on this host and has not since roughly 2026-03-16, which is the last time the
# prediction sections rendered. Hardcoded sibling-repo paths are what rotted; asking the
# package where its own data lives cannot rot the same way, so they are gone rather than
# repointed.

# Best decodable mode by SNR threshold (descending)
MODE_THRESHOLDS = [
    ("SSB",  3),
    ("RTTY", -5),
    ("CW",   -15),
    ("FT8",  -21),
    ("WSPR", -28),
]


# ---------------------------------------------------------------------------
# ClickHouse
# ---------------------------------------------------------------------------

def connect(host: str, port: int):
    return clickhouse_connect.get_client(host=host, port=port)


def run_query(client, name: str, params: dict | None = None) -> list[dict]:
    """Load and execute a SQL file from queries/, return list of row dicts."""
    sql = (QUERIES_DIR / f"{name}.sql").read_text()
    if params:
        sql = sql.format(**params)
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
    return rows


DB_FILE = os.environ.get("HAMSTATS_DB_FILE", "/etc/hamstats/db.dsn")


def load_from_serving() -> tuple[dict, list[str]]:
    """Read the materialised query results out of PostgreSQL.

    Returns ({query_name: rows}, [problems]).

    This replaces running 24 aggregate queries against ClickHouse on every publish --
    123,962,343,315 rows read to produce the 4,398 that get published, eight times a day.
    ClickHouse remains the source of truth; refresh.py materialises these results at a cadence
    matched to how fast each one actually changes.

    A MISSING result is not an empty one. The old code caught a query failure, set the result to
    [] and rendered a page with empty tables on a successful exit; here a query that has never
    been refreshed and one whose result is past its promised max_age are both reported, and the
    caller turns that into a non-zero exit.
    """
    import psycopg

    problems = []
    data = {}
    with psycopg.connect(Path(DB_FILE).read_text().strip()) as conn:
        rows = conn.execute(
            """
            SELECT name, payload, refreshed_at, max_age,
                   now() - refreshed_at        AS age,
                   now() - refreshed_at > max_age AS stale
              FROM serving.query_results
            """
        ).fetchall()
    for name, payload, refreshed_at, max_age, age, stale in rows:
        data[name] = payload
        if stale:
            problems.append(
                f"{name} last refreshed {refreshed_at:%Y-%m-%d %H:%M} UTC "
                f"({age} old, max {max_age}) — the refresh job for its group is not running")

    expected = {q for g in yaml.safe_load((QUERIES_DIR / "cadence.yml").read_text())["groups"].values()
                for q in g["queries"]}
    for missing in sorted(expected - set(data)):
        problems.append(f"{missing} has never been refreshed — no row in serving.query_results")
        data[missing] = []
    return data, problems


def run_all_queries(client) -> dict:
    """Execute every .sql file in queries/ and return {name: rows}."""
    data = {}
    for sql_file in sorted(QUERIES_DIR.glob("*.sql")):
        name = sql_file.stem
        try:
            data[name] = run_query(client, name)
        except Exception as e:
            print(f"  WARNING: {name}.sql failed: {e}")
            data[name] = []
    return data


DATASETS = ("band_summary", "hourly_activity", "solar_timeline", "distance_stats")


def load_recap_from_serving(recap: dict, data: dict) -> dict | None:
    """Read a recap's pre-computed datasets out of the serving layer.

    Recaps used to be aggregated from 1.3 GB of SQLite at render time, off a filesystem that
    existed only on the 9975. That coupling broke every contest page the moment publishing
    moved hosts: the loader warned, returned None, and the run still reported "2 recap(s)
    loaded" and exited 0, so empty pages reached the site unnoticed.

    They are static -- the contests are over -- so they are imported once and served forever.
    Returning None here now means genuinely absent, and the caller treats it as a failure
    rather than as "static findings only".
    """
    got = {}
    for key in DATASETS:
        rows = data.get(f"recap:{recap['slug']}:{key}")
        if rows is None:
            return None
        got[key] = rows
    return got


# ---------------------------------------------------------------------------
# IONIS V22-gamma + PhysicsOverrideLayer Predictions
# ---------------------------------------------------------------------------

def load_ionis_model():
    """Load IONIS V22-gamma model for CPU inference."""
    try:
        import torch  # noqa: F811
        from ionis_validate.model import load_model
        device = torch.device("cpu")
        # No paths: load_model() auto-discovers config_v22.json and the safetensors
        # checkpoint from its own package data.
        model, _config, _meta = load_model(device=device)
        return model, device
    except Exception as e:
        print(f"  ERROR: IONIS model unavailable, predictions will be OMITTED: {e}")
        return None, None


def classify_mode(snr_db: float) -> str:
    for mode, threshold in MODE_THRESHOLDS:
        if snr_db >= threshold:
            return mode
    return "\u2014"


def generate_predictions(model, device, sfi: float, kp: float) -> list[dict] | None:
    """Run V22-gamma + PhysicsOverrideLayer on KI7MT → 6 destinations x 6 bands."""
    if model is None:
        return None
    import torch  # noqa: F811
    from ionis_validate.model import (
        grid4_to_latlon, build_features, haversine_km, BAND_FREQ_HZ, solar_elevation_deg)
    from ionis_validate.physics_override import apply_override_to_prediction

    now = dt.datetime.utcnow()
    hour, month = now.hour, now.month
    day_of_year = now.timetuple().tm_yday
    tx_lat, tx_lon = grid4_to_latlon(TX_GRID)

    results = []
    for dest in PREDICTION_DESTINATIONS:
        rx_lat, rx_lon = grid4_to_latlon(dest["grid"])
        dist_km = haversine_km(tx_lat, tx_lon, rx_lat, rx_lon)
        row = {"label": dest["label"], "bands": {}}
        for band in PREDICTION_BANDS:
            freq_hz = BAND_FREQ_HZ[band]
            features = build_features(
                tx_lat, tx_lon, rx_lat, rx_lon,
                freq_hz, sfi, kp, hour, month,
                day_of_year=day_of_year,
                include_solar_depression=True,
            )
            x = torch.tensor(features, dtype=torch.float32, device=device).unsqueeze(0)
            with torch.no_grad():
                sigma = model(x).item()
            # Apply physics override (Rules A/B: high-band night, Rule C: low-band day)
            freq_mhz = freq_hz / 1e6
            tx_solar = solar_elevation_deg(tx_lat, tx_lon, hour, day_of_year)
            rx_solar = solar_elevation_deg(rx_lat, rx_lon, hour, day_of_year)
            sigma, _ = apply_override_to_prediction(
                sigma, freq_mhz, tx_solar, rx_solar, distance_km=dist_km)
            snr_db = sigma * WSPR_STD_DB + WSPR_MEAN_DB
            row["bands"][band] = classify_mode(snr_db)
        results.append(row)
    return results


def generate_dxpedition_predictions(
    model, device, dxpeditions: list[dict], sfi: float, kp: float,
) -> dict[str, list[dict]] | None:
    """Run V22-gamma + PhysicsOverrideLayer from DN13 to each DXpedition grid across 6 bands.

    Returns {callsign: {"10m": "CW", ...}}.
    """
    if model is None or not dxpeditions:
        return None
    import torch  # noqa: F811
    from ionis_validate.model import (
        grid4_to_latlon, build_features, haversine_km, BAND_FREQ_HZ, solar_elevation_deg)
    from ionis_validate.physics_override import apply_override_to_prediction

    now = dt.datetime.utcnow()
    hour, month = now.hour, now.month
    day_of_year = now.timetuple().tm_yday
    tx_lat, tx_lon = grid4_to_latlon(TX_GRID)

    results = {}
    for dx in dxpeditions:
        grid = dx.get("grid", "")
        if len(grid) < 4:
            continue
        rx_lat, rx_lon = grid4_to_latlon(grid)
        dist_km = haversine_km(tx_lat, tx_lon, rx_lat, rx_lon)
        bands = {}
        for band in PREDICTION_BANDS:
            freq_hz = BAND_FREQ_HZ[band]
            features = build_features(
                tx_lat, tx_lon, rx_lat, rx_lon,
                freq_hz, sfi, kp, hour, month,
                day_of_year=day_of_year,
                include_solar_depression=True,
            )
            x = torch.tensor(features, dtype=torch.float32, device=device).unsqueeze(0)
            with torch.no_grad():
                sigma = model(x).item()
            # Apply physics override (Rules A/B: high-band night, Rule C: low-band day)
            freq_mhz = freq_hz / 1e6
            tx_solar = solar_elevation_deg(tx_lat, tx_lon, hour, day_of_year)
            rx_solar = solar_elevation_deg(rx_lat, rx_lon, hour, day_of_year)
            sigma, _ = apply_override_to_prediction(
                sigma, freq_mhz, tx_solar, rx_solar, distance_km=dist_km)
            snr_db = sigma * WSPR_STD_DB + WSPR_MEAN_DB
            bands[band] = classify_mode(snr_db)
        results[dx["callsign"]] = bands
    return results


# ---------------------------------------------------------------------------
# Contest Recaps (SQLite)
# ---------------------------------------------------------------------------

def load_recaps() -> list[dict]:
    """Load recap definitions from YAML, parse dates."""
    p = ROOT / "data" / "recaps.yaml"
    if not p.exists():
        return []
    with open(p) as f:
        recaps = yaml.safe_load(f) or []
    for r in recaps:
        for field in ("start", "end", "analysis_start", "analysis_end"):
            if isinstance(r.get(field), str):
                r[field] = dt.datetime.fromisoformat(r[field])
    return recaps


def sqlite_ro_uri(db_path: Path) -> str:
    """A URI that opens a contest dataset for reading WITHOUT writing anything.

    The contest datasets live in a directory this process does not own, and the two
    ARRL-DX files are in WAL mode. A WAL database cannot be read at all without creating
    its `-shm` shared-memory sidecar, so a plain sqlite3.connect() raised

        attempt to write a readonly database

    and both recaps were dropped on every publish run — reported as a WARNING and then
    rendered as if the contest simply had no data. `immutable=1` is SQLite's answer for
    exactly this: a database on read-only media, opened with no locking and no sidecar.

    THE TRAP with immutable=1 is that it ignores any `-wal` file, so a database with
    un-checkpointed commits would read back silently STALE — correct-looking numbers that
    are quietly missing the most recent rows. That is worse than the error it replaces, so
    it is only claimed when there is demonstrably no WAL to ignore. If one is present we
    fall back to an ordinary read-only open, which needs a writable directory and will
    fail LOUDLY if it does not have one.
    """
    path = quote(str(db_path))
    if db_path.with_name(db_path.name + "-wal").exists():
        return f"file:{path}?mode=ro"
    return f"file:{path}?mode=ro&immutable=1"


def load_recap_data_sqlite(recap: dict) -> dict | None:
    """Aggregate a recap from its SQLite dataset. USED ONLY BY import_recaps.py.

    This is no longer on the render path. publish.py reads recaps from the serving layer;
    this function exists so the one-time import produces exactly what rendering from SQLite
    produced, using the same code rather than a reimplementation of it.
    """
    """Load aggregated stats from a contest SQLite file.

    Returns dict with band_summary, hourly_activity, solar_timeline,
    distance_stats — or None if the SQLite file is not available.
    """
    dataset = recap.get("dataset")
    if not dataset:
        return None
    db_path = CONTEST_DATA_DIR / dataset
    if not db_path.exists():
        print(f"  WARNING: contest dataset not found: {db_path}")
        return None

    source = recap.get("primary_source", "pskr")
    table = f"{source}_signatures"

    try:
        conn = sqlite3.connect(sqlite_ro_uri(db_path), uri=True)
        conn.row_factory = sqlite3.Row
        data = {}

        # Band summary: signature counts, median SNR, avg distance, peak hour
        rows = conn.execute(f"""
            SELECT band, COUNT(*) as sig_count,
                   ROUND(AVG(median_snr), 1) as median_snr,
                   ROUND(AVG(avg_distance), 0) as avg_distance,
                   (SELECT hour FROM {table} t2
                    WHERE t2.band = t1.band
                    GROUP BY hour ORDER BY SUM(spot_count) DESC LIMIT 1
                   ) as peak_hour
            FROM {table} t1
            GROUP BY band
            ORDER BY band
        """).fetchall()
        band_summary = []
        for r in rows:
            bname = ADIF_TO_BAND.get(r["band"], str(r["band"]))
            band_summary.append({
                "band": bname,
                "sig_count": r["sig_count"],
                "median_snr": r["median_snr"],
                "avg_distance": r["avg_distance"],
                "peak_hour": r["peak_hour"],
            })
        data["band_summary"] = band_summary

        # Hourly activity: pivot by band × hour
        bands_of_interest = recap.get("bands_of_interest", [])
        band_adifs = {BAND_TO_ADIF[b]: b for b in bands_of_interest if b in BAND_TO_ADIF}
        if band_adifs:
            rows = conn.execute(f"""
                SELECT hour, band, SUM(spot_count) as spots
                FROM {table}
                WHERE band IN ({','.join(str(a) for a in band_adifs)})
                GROUP BY hour, band
                ORDER BY hour, band
            """).fetchall()
            hourly = {}
            for r in rows:
                h = r["hour"]
                if h not in hourly:
                    hourly[h] = {"hour": h, "bands": {}}
                bname = ADIF_TO_BAND.get(r["band"], str(r["band"]))
                hourly[h]["bands"][bname] = r["spots"]
            data["hourly_activity"] = [hourly[h] for h in sorted(hourly)]

        # Solar timeline
        try:
            rows = conn.execute("""
                SELECT date, sfi, ssn, kp, ap
                FROM solar_timeline
                ORDER BY date
            """).fetchall()
            data["solar_timeline"] = [
                {"date": r["date"], "sfi": r["sfi"], "ssn": r["ssn"],
                 "kp": round(r["kp"], 2) if r["kp"] else None,
                 "ap": r["ap"]}
                for r in rows
            ]
        except sqlite3.OperationalError:
            data["solar_timeline"] = []

        # Distance stats per band
        rows = conn.execute(f"""
            SELECT band,
                   ROUND(MIN(avg_distance), 0) as min_dist,
                   ROUND(AVG(avg_distance), 0) as median_dist,
                   ROUND(MAX(avg_distance), 0) as max_dist,
                   COUNT(DISTINCT tx_grid_4 || rx_grid_4) as path_count
            FROM {table}
            GROUP BY band
            ORDER BY band
        """).fetchall()
        data["distance_stats"] = [
            {"band": ADIF_TO_BAND.get(r["band"], str(r["band"])),
             "min_dist": r["min_dist"], "median_dist": r["median_dist"],
             "max_dist": r["max_dist"], "path_count": r["path_count"]}
            for r in rows
        ]

        conn.close()
        return data

    except Exception as e:
        print(f"  WARNING: failed to load recap data from {db_path}: {e}")
        return None


# ---------------------------------------------------------------------------
# Jinja2 Filters
# ---------------------------------------------------------------------------

def fmt(n) -> str:
    """Format number: 10916787061 → '10.92B', 354221455 → '354.2M'."""
    if n is None or isinstance(n, Undefined):
        return "\u2014"
    try:
        n = float(n)
    except (TypeError, ValueError):
        return "\u2014"
    if n != n:  # NaN
        return "\u2014"
    if abs(n) >= 1_000_000_000:
        return f"{n / 1_000_000_000:.2f}B"
    if abs(n) >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if abs(n) >= 1_000:
        return f"{int(n):,}"
    if n == int(n):
        return str(int(n))
    return f"{n:.2f}"


def fmt_pct(n) -> str:
    if n is None or isinstance(n, Undefined):
        return "\u2014"
    try:
        return f"{float(n):.2f}%"
    except (TypeError, ValueError):
        return str(n)


def fmt_date(d) -> str:
    if d is None or isinstance(d, Undefined):
        return "\u2014"
    if hasattr(d, "strftime"):
        return d.strftime("%Y-%m-%d")
    return str(d)


def fmt_snr(snr) -> str:
    if snr is None or isinstance(snr, Undefined):
        return "\u2014"
    try:
        v = int(snr)
        return f"+{v} dB" if v >= 0 else f"{v} dB"
    except (TypeError, ValueError):
        return str(snr)


def fmt_delta(val) -> str:
    if val is None or isinstance(val, Undefined):
        return "\u2014"
    try:
        v = float(val)
    except (TypeError, ValueError):
        return str(val)
    if v > 0:
        return f"+{int(v)}" if v == int(v) else f"+{v:.1f}"
    if v < 0:
        return f"{int(v)}" if v == int(v) else f"{v:.1f}"
    return "0"


def classify_kp(kp) -> str:
    if kp is None:
        return "\u2014"
    try:
        kp = float(kp)
    except (TypeError, ValueError):
        return "\u2014"
    if kp < 3:
        return "Quiet"
    if kp < 4:
        return "Unsettled"
    if kp < 5:
        return "Active"
    if kp < 6:
        return "G1 Storm"
    if kp < 7:
        return "G2 Storm"
    if kp < 8:
        return "G3 Storm"
    if kp < 9:
        return "G4 Storm"
    return "G5 Storm"


def classify_sfi(sfi) -> str:
    if sfi is None:
        return "\u2014"
    try:
        sfi = float(sfi)
    except (TypeError, ValueError):
        return "\u2014"
    if sfi < 80:
        return "Low"
    if sfi < 120:
        return "Moderate"
    if sfi < 150:
        return "Elevated"
    if sfi < 200:
        return "High"
    return "Very High"


def kp_impact(kp) -> str:
    if kp is None:
        return "\u2014"
    try:
        kp = float(kp)
    except (TypeError, ValueError):
        return "\u2014"
    if kp < 3:
        return "Normal"
    if kp < 4:
        return "Minor"
    if kp < 5:
        return "Moderate"
    if kp < 6:
        return "Degraded"
    if kp < 7:
        return "Significant"
    return "Severe"


def band_status(total_spots) -> str:
    if total_spots is None:
        return "Closed"
    try:
        n = int(total_spots)
    except (TypeError, ValueError):
        return "\u2014"
    if n == 0:
        return "Closed"
    if n < 1_000:
        return "Marginal"
    if n < 50_000:
        return "Open"
    return "Strong"


def fmt_countdown(days) -> str:
    """Format days until event: 'NOW', '3 days', '2w 1d', etc."""
    if days is None:
        return "\u2014"
    try:
        d = float(days)
    except (TypeError, ValueError):
        return str(days)
    if d <= 0:
        return "NOW"
    d = int(d)
    if d == 1:
        return "1 day"
    if d < 14:
        return f"{d} days"
    weeks = d // 7
    remaining = d % 7
    if remaining == 0:
        return f"{weeks}w"
    return f"{weeks}w {remaining}d"


def fmt_utc(d) -> str:
    """Format datetime as 'YYYY-MM-DD HH:MM UTC'."""
    if d is None or isinstance(d, Undefined):
        return "\u2014"
    if hasattr(d, "strftime"):
        return d.strftime("%Y-%m-%d %H:%M UTC")
    return str(d)


# ---------------------------------------------------------------------------
# Context Building
# ---------------------------------------------------------------------------

# How stale each source can legitimately be, in days, and why.
#
# A single global threshold ("1 day = Current, anything more = behind") marked healthy
# sources as late. RBN publishes each day's archive the FOLLOWING day and rbn-download.timer
# fetches at 16:00 UTC with rbn-ingest at 16:30 — so for most of the day the freshest value
# RBN can possibly have is T-2, and the table reported "2 days behind" every morning with
# nothing wrong. It flipped to "Current" at 16:30 and back at midnight, daily, forever.
#
# Expectations are per source because the sources are not alike: two are live streams, one
# is a next-day archive, and one is a next-day archive we only fetch once a day.
LIVE_SOURCES = ("PSK Reporter", "Solar")     # continuous ingest — same-day or it is late
NEXT_DAY_SOURCES = ("WSPR",)                 # upstream publishes T-1

# RBN's expectation is time-of-day dependent, which a flat number cannot express. Before the
# fetch+ingest window closes, T-2 is correct; after it, we should have T-1. Using a flat 2
# would keep the label honest but would also hide a genuinely missed fetch — which is the
# failure this column exists to surface.
RBN_INGEST_COMPLETE_HOUR = 17                # rbn-download 16:00, rbn-ingest 16:30, +margin


def expected_lag_days(name: str, now: dt.datetime) -> int:
    """Largest age, in days, that is NORMAL for this source at this moment."""
    if name in LIVE_SOURCES:
        return 0
    if name in NEXT_DAY_SOURCES:
        return 1
    if name == "RBN":
        return 1 if now.hour >= RBN_INGEST_COMPLETE_HOUR else 2
    return 1                                  # unknown source: the old default


def enrich_bronze_status(data: dict, now: dt.datetime):
    """Add latest_display and status fields to bronze_status rows."""
    today = now.date()
    for row in data.get("bronze_status", []):
        name = row.get("source_name", "")
        latest = row.get("latest_date")
        if name == "Contest":
            row["latest_display"] = "Archive"
            row["status"] = "Static"
            continue
        if latest is None:
            row["latest_display"] = "\u2014"
            row["status"] = "\u2014"
            continue
        if hasattr(latest, "date"):
            d = latest.date()
        elif isinstance(latest, dt.date):
            d = latest
        else:
            try:
                d = dt.date.fromisoformat(str(latest)[:10])
            except ValueError:
                row["latest_display"] = str(latest)
                row["status"] = "\u2014"
                continue
        row["latest_display"] = d.strftime("%Y-%m-%d")
        delta = (today - d).days
        expected = expected_lag_days(name, now)
        if delta <= 0:
            row["status"] = "Live"
        elif delta <= expected:
            row["status"] = "Current"
        else:
            # Report lateness RELATIVE TO THE EXPECTATION, so "1 day behind" means one day
            # later than this source should be — not one day past an arbitrary line that
            # several healthy sources were never going to meet.
            late = delta - expected
            row["status"] = f"{late} day behind" if late == 1 else f"{late} days behind"


def build_context(
    data: dict,
    predictions,
    now: dt.datetime,
    contest_schedule=None,
    upcoming_30d=None,
    full_year=None,
    dxpeditions=None,
    dx_calendars=None,
    dxpedition_predictions=None,
) -> dict:
    """Assemble the full Jinja2 template context."""
    enrich_bronze_status(data, now)

    solar = data.get("solar_current", [{}])
    solar_row = solar[0] if solar else {}
    raw_sfi = solar_row.get("solar_flux")
    raw_kp = solar_row.get("kp_index")
    sfi = int(raw_sfi) if raw_sfi is not None and raw_sfi == int(raw_sfi) else raw_sfi
    kp = round(float(raw_kp), 2) if raw_kp is not None else raw_kp
    conditions = solar_row.get("conditions", "\u2014")
    # Store display-friendly values back into the solar row
    solar_row["solar_flux"] = sfi
    solar_row["kp_index"] = kp

    # Band activity lookup: band_name → row dict
    band_activity = {}
    for row in data.get("band_activity_24h", []):
        bname = row.get("band_name")
        if bname:
            band_activity[bname] = row

    return {
        "now": now,
        "data": data,
        "sfi": sfi,
        "kp": kp,
        "conditions": conditions,
        "predictions": predictions,
        "bands": BANDS,
        "prediction_bands": PREDICTION_BANDS,
        "band_activity": band_activity,
        "adif_to_band": ADIF_TO_BAND,
        "contest_schedule": contest_schedule or [],
        "upcoming_30d": upcoming_30d or [],
        "full_year": full_year or [],
        "dxpeditions": dxpeditions or [],
        "dx_calendars": dx_calendars or [],
        "dxpedition_predictions": dxpedition_predictions or {},
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_all(
    env: Environment, context: dict, recaps: list[dict] | None = None,
) -> dict[str, str]:
    """Render all templates, return {relative_path: content}."""
    outputs = {}

    # 1:1 templates
    simple = [
        "index.md.j2",
        "bands/index.md.j2",
        "solar/index.md.j2",
        "solar/current.md.j2",
        "solar/storms.md.j2",
        "solar/cycle.md.j2",
        "sources/index.md.j2",
        "sources/wspr.md.j2",
        "sources/rbn.md.j2",
        "sources/pskr.md.j2",
        "sources/contest.md.j2",
        "dataset/index.md.j2",
        "dataset/growth.md.j2",
        "dataset/coverage.md.j2",
        "contests/index.md.j2",
        "contests/dxpeditions.md.j2",
        "loggers/index.md.j2",
        "loggers/participation.md.j2",
    ]
    for tmpl_name in simple:
        out_name = tmpl_name.removesuffix(".j2")
        tmpl = env.get_template(tmpl_name)
        outputs[out_name] = tmpl.render(**context)

    # Band template × 9
    band_tmpl = env.get_template("bands/band.md.j2")
    for band in BANDS:
        out_name = f"bands/{band['name']}.md"
        outputs[out_name] = band_tmpl.render(**context, band=band)

    # Contest recap pages
    if recaps:
        recap_tmpl = env.get_template("contests/recap.md.j2")
        for recap, recap_data in recaps:
            out_name = f"contests/{recap['slug']}.md"
            outputs[out_name] = recap_tmpl.render(
                **context, recap=recap, recap_data=recap_data,
            )

    return outputs


def write_outputs(outputs: dict[str, str]) -> list[str]:
    """Write rendered content to docs/, return list of changed paths."""
    changed = []
    for relpath, content in sorted(outputs.items()):
        if relpath in STATIC_PATHS:
            continue
        outpath = DOCS_DIR / relpath
        outpath.parent.mkdir(parents=True, exist_ok=True)
        if outpath.exists() and outpath.read_text() == content:
            continue
        outpath.write_text(content)
        changed.append(relpath)
    return changed


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------

def git_push(changed: list[str]):
    if not changed:
        print("No changes to commit.")
        return
    # The content repo, not the install dir — /usr/share is not a git checkout.
    os.chdir(CONTENT_DIR)
    subprocess.run(["git", "add", "docs/"], check=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode == 0:
        print("No staged changes — nothing to commit.")
        return
    stamp = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    msg = f"publish: update site data ({stamp})"
    subprocess.run(["git", "commit", "-m", msg], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"Pushed {len(changed)} changed file(s).")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Ham Stats publish pipeline")
    ap.add_argument("--push", action="store_true",
                    help="Commit and push after render")
    ap.add_argument("--build", action="store_true",
                    help="Run mkdocs build after render")
    ap.add_argument("--dry-run", action="store_true",
                    help="List what would change, no writes")
    ap.add_argument("--host", default="192.168.1.90",
                    help="ClickHouse host (default: 192.168.1.90)")
    ap.add_argument("--port", type=int, default=8123,
                    help="ClickHouse HTTP port (default: 8123)")
    ap.add_argument("--from-clickhouse", action="store_true",
                    help="query ClickHouse directly instead of the PostgreSQL serving layer "
                         "(the pre-serving-layer path; kept so the two can be compared)")
    args = ap.parse_args()

    now = dt.datetime.utcnow()
    print(f"Ham Stats publish — {now.strftime('%Y-%m-%d %H:%M UTC')}")

    # 1. Query results
    stale = []
    if args.from_clickhouse:
        print("Connecting to ClickHouse...")
        client = connect(args.host, args.port)
        print("Running queries...")
        data = run_all_queries(client)
    else:
        print("Reading the PostgreSQL serving layer...")
        data, stale = load_from_serving()
    for name, rows in data.items():
        print(f"  {name}: {len(rows)} row(s)")
    for p in stale:
        print(f"  STALE: {p}", file=sys.stderr)

    # 2. IONIS predictions
    solar = data.get("solar_current", [{}])
    solar_row = solar[0] if solar else {}
    # NO DEFAULTS. This was:
    #
    #     sfi = float(solar_row.get("solar_flux", 100))
    #     kp  = float(solar_row.get("kp_index", 3))
    #
    # wspr.live_conditions was an ENGINE = Memory table, so it was EMPTY for up to
    # fifteen minutes after every ClickHouse restart. solar_current then returned no
    # rows, those defaults fired, and the IONIS model produced a full set of band
    # predictions from an SFI and Kp nobody measured — published as current conditions
    # while the indices beside them rendered as em-dashes.
    #
    # SFI and Kp are the model's two space-weather inputs. Substituting them does not
    # degrade the prediction, it fabricates it. Without real values there is nothing
    # honest to predict, so we do not.
    raw_sfi, raw_kp = solar_row.get("solar_flux"), solar_row.get("kp_index")
    sfi = float(raw_sfi) if raw_sfi is not None else None
    kp = float(raw_kp) if raw_kp is not None else None

    predictions = None
    model = device = None      # both consumed again by the DXpedition pass below
    if sfi is None or kp is None:
        print("  ERROR: no live solar conditions (wspr.live_conditions returned "
              f"{len(solar)} row(s)); predictions REQUIRE real SFI and Kp and are "
              "skipped rather than run on substituted values.", file=sys.stderr)
    else:
        print("Loading IONIS V22-gamma model...")
        model, device = load_ionis_model()
        predictions = generate_predictions(model, device, sfi, kp)
    if predictions:
        print(f"  Generated {len(predictions)} destination predictions")
    else:
        print("  Predictions skipped")

    # 3. Render templates
    print("Rendering templates...")
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["fmt"] = fmt
    env.filters["fmt_pct"] = fmt_pct
    env.filters["fmt_date"] = fmt_date
    env.filters["fmt_snr"] = fmt_snr
    env.filters["fmt_delta"] = fmt_delta
    env.filters["classify_kp"] = classify_kp
    env.filters["classify_sfi"] = classify_sfi
    env.filters["kp_impact"] = kp_impact
    env.filters["band_status"] = band_status
    env.filters["fmt_countdown"] = fmt_countdown
    env.filters["fmt_utc"] = fmt_utc

    # 4. Contest calendar + DXpeditions
    print("Loading contest calendar...")
    contests_data = contest_calendar.load_contests()
    full_year = contest_calendar.build_contest_schedule(contests_data, now)
    upcoming_30d = contest_calendar.upcoming_contests(full_year, days=30)
    print(f"  {len(full_year)} contest dates resolved, {len(upcoming_30d)} in next 30 days")

    dx_data = contest_calendar.load_dxpeditions()
    dx_calendars = dx_data.get("calendars", [])
    dx_list = contest_calendar.build_dxpedition_schedule(
        dx_data.get("dxpeditions", []), now,
    )
    print(f"  {len(dx_list)} active/upcoming DXpeditions")

    # DXpedition predictions
    dx_predictions = generate_dxpedition_predictions(model, device, dx_list, sfi, kp)
    if dx_predictions:
        print(f"  Generated predictions for {len(dx_predictions)} DXpeditions")

    # 5. Contest recaps — pre-imported into the serving layer, not read from SQLite
    print("Loading contest recaps...")
    recap_defs = load_recaps()
    recaps = []
    for recap in recap_defs:
        recap_data = load_recap_from_serving(recap, data)
        if recap_data:
            print(f"  {recap['slug']}: {len(recap_data.get('band_summary', []))} bands")
        else:
            # NOT "static findings only". That wording made an absent dataset look like a
            # deliberate mode, and the count below counted DEFINITIONS regardless — so two
            # empty contest pages published cleanly and nothing said otherwise.
            print(f"  {recap['slug']}: NOT IMPORTED — page will render without band data",
                  file=sys.stderr)
            stale.append(f"recap {recap['slug']} has no data in the serving layer "
                         f"(run import_recaps.py for it)")
        recaps.append((recap, recap_data))
    print(f"  {sum(1 for _, d in recaps if d)} of {len(recaps)} recap(s) have data")

    context = build_context(
        data, predictions, now,
        contest_schedule=full_year,
        upcoming_30d=upcoming_30d,
        full_year=full_year,
        dxpeditions=dx_list,
        dx_calendars=dx_calendars,
        dxpedition_predictions=dx_predictions or {},
    )
    outputs = render_all(env, context, recaps=recaps)

    if args.dry_run:
        print(f"\nDry run — {len(outputs)} files would be rendered:")
        for f in sorted(outputs):
            marker = " (static, skipped)" if f in STATIC_PATHS else ""
            print(f"  docs/{f}{marker}")
        return

    # 4. Write to docs/
    changed = write_outputs(outputs)
    print(f"Rendered {len(outputs)} files, {len(changed)} changed.")
    for f in changed:
        print(f"  changed: docs/{f}")

    # 5. Optional post-render actions
    if args.build:
        print("Building site with mkdocs...")
        subprocess.run(
            [sys.executable, "-m", "mkdocs", "build"],
            cwd=CONTENT_DIR, check=True,
        )

    if args.push:
        git_push(changed)

    print("Done.")

    # PUBLISH FIRST, THEN COMPLAIN. The data pages are worth shipping even when the model
    # is down, so this does not abort the run — but a missing model silently removes the
    # site's headline feature ("What Can You Work Right Now?", the contest prediction table
    # and the DXpedition bands all sit behind `{% if predictions %}`), and the only trace
    # was one WARNING line in a log nobody reads. That is how this went unnoticed from
    # 2026-03-16 until someone happened to read the journal.
    #
    # Exiting non-zero puts the unit in `failed`, which is a signal that survives not being
    # watched. Set HAMSTATS_PREDICTIONS=off to publish without them deliberately.
    if stale:
        # Published first, as with the model: last-good numbers beat no page at all. But the
        # unit lands in `failed`, because a serving layer nobody notices has gone stale is
        # strictly worse than no serving layer — it looks current.
        print(f"ERROR: published with {len(stale)} stale or missing result(s); "
              "the site is showing data older than its refresh cadence promises.",
              file=sys.stderr)
        return 1

    if model is None and os.environ.get("HAMSTATS_PREDICTIONS", "on").lower() != "off":
        print("ERROR: published without IONIS predictions — the prediction sections are "
              "missing from the site. Install ionis-validate into this interpreter, or set "
              "HAMSTATS_PREDICTIONS=off if that is intended.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
