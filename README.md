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

## Site Sections

| Section | Content |
|---------|---------|
| **Bands** | Per-band propagation reports (160m–10m) with spot volume, SNR, and geographic reach |
| **Solar** | Current conditions, storm impact analysis (actual dB cost), solar cycle tracking |
| **Sources** | Per-source statistics, growth rates, and collection status |
| **Dataset** | Total row counts, daily growth, geographic coverage |
| **Contests** | Weekend recaps with spot volume spikes and band breakdowns |
| **Methodology** | How raw spots become signatures, data quality filtering |

## Building Locally

```bash
pip install mkdocs-material
mkdocs serve
```

Open `http://localhost:8000` to preview.

## Publishing

The publish workflow runs on a cron schedule:

1. Query ClickHouse for current data
2. Inject results into page templates (replacing `<!-- AUTO-GENERATED -->` markers)
3. `mkdocs build`
4. Push to `gh-pages` branch
5. GitHub Pages rebuilds automatically

## Part of the IONIS Project

Ham Stats is a product of [IONIS-AI](https://github.com/IONIS-AI) — the Ionospheric Neural Inference System. The model and data documentation live at [ionis-docs](https://github.com/IONIS-AI/ionis-docs). User-facing tools (CLI, dashboards) live at [ionis-tools](https://github.com/IONIS-AI/ionis-tools).

## License

GPL-3.0 — see [LICENSE](LICENSE).
