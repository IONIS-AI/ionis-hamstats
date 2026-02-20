# Ham Stats

**HF propagation reports generated from real data — not models, not opinions.**

Every number on this site comes from measured amateur radio observations: WSPR
beacons, Reverse Beacon Network skimmers, PSK Reporter decodes, and contest
logs. Solar conditions are correlated with actual signal measurements, not
theoretical predictions.

---

## Current Conditions

<!-- AUTO-GENERATED: solar conditions block -->

| Metric | Value | Status |
|--------|-------|--------|
| **SFI** | 116 | Moderate |
| **Kp** | 2.33 | Quiet |
| **Conditions** | Quiet | Normal propagation |

*Updated every 3 hours from NOAA SWPC via ClickHouse.*

---

## Data Pipeline

<!-- AUTO-GENERATED: bronze table status -->

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-02-19 | 10.92B | Current |
| RBN | 2026-02-18 | 2.25B | 1 day behind |
| PSK Reporter | 2026-02-20 | 354M | Live |
| Contest | Archive | 234M | Static |
| Solar | 2026-02-20 | 76.9K | Live |

---

## Band Activity (Last 24 Hours)

<!-- AUTO-GENERATED: band activity summary -->

*Which bands had propagation in the last 24 hours, based on spots from all sources.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | 71,718 | — | 5,596,149 | +61 dB | Open |
| 12m | 35,919 | — | 1,680,441 | +59 dB | Open |
| 15m | 100,070 | — | 4,044,066 | +87 dB | Strong |
| 17m | 100,789 | — | 1,800,918 | +62 dB | Open |
| 20m | 400,496 | — | 7,595,376 | +65 dB | Strong |
| 30m | 167,179 | — | 2,042,957 | +58 dB | Open |
| 40m | 237,134 | — | 7,329,802 | +86 dB | Strong |
| 80m | 119,072 | — | 1,860,231 | +87 dB | Strong |
| 160m | 33,668 | — | 277,565 | +54 dB | Open |

---

## About This Site

Ham Stats is generated every 3 hours from a self-hosted ClickHouse database
containing **13+ billion** amateur radio propagation observations — the largest
curated dataset of its kind on Earth. No cloud services. No third-party APIs.
Every query runs against data we collected and maintain.

The data comes from four independent networks, each measuring a different layer
of HF propagation:

- **WSPR** (10.9B spots, 2008–present) — the SNR floor at minimum power
- **Reverse Beacon Network** (2.25B spots, 2009–present) — CW/RTTY measured signals
- **PSK Reporter** (354M spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*
