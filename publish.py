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
import subprocess
import sys
from pathlib import Path
from typing import Optional

import clickhouse_connect
import yaml
from jinja2 import Environment, FileSystemLoader, Undefined

import contest_calendar

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent
QUERIES_DIR = ROOT / "queries"
TEMPLATES_DIR = ROOT / "templates"
DOCS_DIR = ROOT / "docs"

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
_TRAINING_DIR = Path("/mnt/ai-stack/ionis-ai/ionis-training")
_COMMON_DIR = _TRAINING_DIR / "versions" / "common"
_V22_CONFIG = _TRAINING_DIR / "versions" / "v22" / "config_v22.json"
_V22_CHECKPOINT = _TRAINING_DIR / "versions" / "v22" / "ionis_v22_gamma.safetensors"

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
                # Round Float32 precision artifacts (e.g. 2.329999 → 2.33)
                v = round(v, 2)
            d[col] = v
        rows.append(d)
    return rows


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


# ---------------------------------------------------------------------------
# IONIS V22-gamma + PhysicsOverrideLayer Predictions
# ---------------------------------------------------------------------------

def load_ionis_model():
    """Load IONIS V22-gamma model for CPU inference."""
    try:
        import torch  # noqa: F811
        sys.path.insert(0, str(_COMMON_DIR))
        from model import load_model
        device = torch.device("cpu")
        model, _config, _meta = load_model(
            config_path=str(_V22_CONFIG),
            checkpoint_path=str(_V22_CHECKPOINT),
            device=device,
        )
        return model, device
    except Exception as e:
        print(f"  WARNING: IONIS model not available: {e}")
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
    from model import grid4_to_latlon, build_features, haversine_km, BAND_FREQ_HZ, solar_elevation_deg
    from physics_override import apply_override_to_prediction

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
    from model import grid4_to_latlon, build_features, haversine_km, BAND_FREQ_HZ, solar_elevation_deg
    from physics_override import apply_override_to_prediction

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
        if delta <= 0:
            row["status"] = "Live"
        elif delta == 1:
            row["status"] = "Current"
        else:
            row["status"] = f"{delta} days behind"


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

def render_all(env: Environment, context: dict) -> dict[str, str]:
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
    os.chdir(ROOT)
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
    args = ap.parse_args()

    now = dt.datetime.utcnow()
    print(f"Ham Stats publish — {now.strftime('%Y-%m-%d %H:%M UTC')}")

    # 1. ClickHouse queries
    print("Connecting to ClickHouse...")
    client = connect(args.host, args.port)
    print("Running queries...")
    data = run_all_queries(client)
    for name, rows in data.items():
        print(f"  {name}: {len(rows)} row(s)")

    # 2. IONIS predictions
    solar = data.get("solar_current", [{}])
    solar_row = solar[0] if solar else {}
    sfi = float(solar_row.get("solar_flux", 100))
    kp = float(solar_row.get("kp_index", 3))
    print("Loading IONIS V22-gamma model...")
    model, device = load_ionis_model()
    predictions = generate_predictions(model, device, sfi, kp)
    if predictions:
        print(f"  Generated {len(predictions)} destination predictions")
    else:
        print("  Predictions skipped (model not available)")

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

    context = build_context(
        data, predictions, now,
        contest_schedule=full_year,
        upcoming_30d=upcoming_30d,
        full_year=full_year,
        dxpeditions=dx_list,
        dx_calendars=dx_calendars,
        dxpedition_predictions=dx_predictions or {},
    )
    outputs = render_all(env, context)

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
            cwd=ROOT, check=True,
        )

    if args.push:
        git_push(changed)

    print("Done.")


if __name__ == "__main__":
    main()
