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
| **SFI** | — | — |
| **Kp** | — | — |
| **Conditions** | — | — |

*Updated every 3 hours from NOAA SWPC via ClickHouse.*

---

## Data Pipeline

<!-- AUTO-GENERATED: bronze table status -->

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | — | — | — |
| RBN | — | — | — |
| PSK Reporter | — | — | — |
| Contest | — | — | — |
| Solar | — | — | — |

---

## Band Activity (Last 24 Hours)

<!-- AUTO-GENERATED: band activity summary -->

*Which bands had propagation in the last 24 hours, based on spots from all sources.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | — | — | — | — | — |
| 15m | — | — | — | — | — |
| 20m | — | — | — | — | — |
| 40m | — | — | — | — | — |
| 80m | — | — | — | — | — |
| 160m | — | — | — | — | — |

---

## About This Site

Ham Stats is generated every 3 hours from a self-hosted ClickHouse database
containing **13+ billion** amateur radio propagation observations — the largest
curated dataset of its kind on Earth. No cloud services. No third-party APIs.
Every query runs against data we collected and maintain.

The data comes from four independent networks, each measuring a different layer
of HF propagation:

- **WSPR** (10.8B spots, 2008–present) — the SNR floor at minimum power
- **Reverse Beacon Network** (2.2B spots, 2009–present) — CW/RTTY measured signals
- **PSK Reporter** (26M spots/day, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (195M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*
