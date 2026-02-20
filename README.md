# ionis-hamstats

**Source for [ham-stats.com](https://ham-stats.com)** — HF propagation reports generated from real data.

## What Is This?

A static site built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) that publishes HF band conditions, solar impact analysis, and propagation reports. Every number comes from measured amateur radio observations — not models, not opinions.

The site is auto-generated every 3 hours from a ClickHouse database containing **13+ billion** propagation observations across four independent networks:

| Source | Volume | What It Measures |
|--------|--------|-----------------|
| **WSPR** | 10.9B spots (2008–present) | SNR floor at minimum power (~200 mW) |
| **Reverse Beacon Network** | 2.25B spots (2009–present) | CW/RTTY measured signals |
| **PSK Reporter** | 26M spots/day (live, Feb 2026+) | FT8/digital operational contacts |
| **Contest Logs** | 234M QSOs (2005–present) | SSB/RTTY ceiling at contest power |

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every measurement has its solar context.

## Publish Pipeline

The site is fully automated via `publish.py` — a Jinja2 template engine that queries ClickHouse, renders markdown, and pushes to GitHub where Actions deploys via `mkdocs gh-deploy`.

```
ClickHouse (13B+ spots)
    ↓
queries/*.sql (15 SQL files)
    ↓
publish.py → Jinja2 render
    ↓
templates/**/*.md.j2 (16 templates → 24 pages)
    ↓
docs/*.md (generated output)
    ↓
git push → GH Actions → mkdocs gh-deploy → ham-stats.com
```

**CLI usage:**

```bash
python publish.py              # render only (preview)
python publish.py --push       # render + commit + push
python publish.py --build      # render + mkdocs build (local preview)
python publish.py --dry-run    # list what would change
python publish.py --host X     # custom ClickHouse host (default: 192.168.1.90)
```

**Cron (9975WX):**

```
0 */3 * * * .venv/bin/python publish.py --push 2>&1 | logger -t hamstats-publish
```

## IONIS V20 Predictions

The homepage includes a live prediction table from the IONIS V20 model (IonisGate, 203K params). For each publish cycle, the model predicts SNR from KI7MT (DN26) to six representative contest destinations across four bands, using the current SFI and Kp from `wspr.live_conditions`.

Predicted SNR is classified into the best decodable mode:

| Mode | SNR Threshold |
|------|--------------|
| SSB | >= +3 dB |
| RTTY | >= -5 dB |
| CW | >= -15 dB |
| FT8 | >= -21 dB |
| WSPR | >= -28 dB |
| Closed | < -28 dB |

The model loads from [ionis-validate](https://github.com/IONIS-AI/ionis-validate) — 24 inferences per cycle, under 1 second on CPU.

## Project Structure

```
ionis-hamstats/
├── publish.py              # Main script: query → render → push
├── requirements.txt        # mkdocs-material, clickhouse-connect, Jinja2
├── mkdocs.yml              # MkDocs Material configuration
├── queries/                # SQL files (15), one per logical query
│   ├── solar_current.sql
│   ├── bronze_status.sql
│   ├── band_activity_24h.sql
│   ├── sfi_trend_7d.sql
│   ├── kp_trend_7d.sql
│   └── ...
├── templates/              # Jinja2 source templates (16 → 24 pages)
│   ├── index.md.j2
│   ├── bands/
│   │   ├── index.md.j2
│   │   └── band.md.j2     # Rendered 9x (one per HF band)
│   ├── solar/
│   ├── sources/
│   ├── dataset/
│   └── contests/
└── docs/                   # Generated output (committed, deployed)
    ├── about.md            # Static — never overwritten
    ├── methodology/        # Static — never overwritten
    └── (everything else generated from templates/)
```

## Site Sections

| Section | Content |
|---------|---------|
| **Home** | Color-coded SFI/Kp badges, data pipeline status, band activity, IONIS predictions |
| **Bands** | Per-band propagation reports (160m–10m) with spot volume, SNR, and solar context |
| **Solar** | Current conditions, 7-day trends, storm impact analysis, solar cycle tracking |
| **Sources** | Per-source statistics (WSPR, RBN, PSKR, Contest) with band/mode breakdowns |
| **Dataset** | Total row counts, growth tracking, geographic coverage |
| **Contests** | Weekend recaps with spot volume spikes and band breakdowns |
| **Methodology** | How raw spots become signatures, data quality filtering |

## Building Locally

```bash
python -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python publish.py --build
mkdocs serve
```

Open `http://localhost:8000` to preview. Requires ClickHouse access for live data.

## Part of the IONIS Project

Ham Stats is a product of [IONIS-AI](https://github.com/IONIS-AI) — the Ionospheric Neural Inference System. The model and data documentation live at [ionis-docs](https://github.com/IONIS-AI/ionis-docs). User-facing tools (CLI, dashboards) live at [ionis-tools](https://github.com/IONIS-AI/ionis-tools).

## License

GPL-3.0 — see [LICENSE](LICENSE).
