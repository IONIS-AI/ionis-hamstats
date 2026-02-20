# Ham Stats

**HF propagation reports generated from real data — not models, not opinions.**

Every number on this site comes from measured amateur radio observations: WSPR
beacons, Reverse Beacon Network skimmers, PSK Reporter decodes, and contest
logs. Solar conditions are correlated with actual signal measurements, not
theoretical predictions.

---

## Current Conditions

!!! info inline "SFI 116"
    Moderate

!!! success inline end "Kp 2.33"
    Quiet

<div style="clear: both;"></div>

*Quiet · Updated 20:40 UTC from NOAA SWPC*

---

## Data Pipeline

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-02-19 | 10.92B | Current |
| RBN | 2026-02-18 | 2.25B | 2 days behind |
| PSK Reporter | 2026-02-20 | 356.2M | Live |
| Contest | Archive | 234.3M | Static |
| Solar | 2026-02-20 | 76,628 | Live |

---

## Band Activity (Last 24 Hours)

*Which bands had propagation in the last 24 hours, based on spots from all sources.
RBN archives lag ~24 hours; zeroes indicate no data in the window, not band closure.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | 49,423 | 0 | 5.7M | +61 dB | Strong |
| 12m | 23,974 | 0 | 1.7M | +59 dB | Strong |
| 15m | 70,743 | 0 | 4.1M | +87 dB | Strong |
| 17m | 72,163 | 0 | 1.8M | +62 dB | Strong |
| 20m | 286,522 | 0 | 7.6M | +80 dB | Strong |
| 30m | 120,399 | 0 | 2.1M | +58 dB | Strong |
| 40m | 170,038 | 0 | 7.3M | +86 dB | Strong |
| 80m | 90,177 | 0 | 1.8M | +87 dB | Strong |
| 160m | 25,543 | 0 | 262,498 | +54 dB | Strong |

---

## IONIS Predictions — KI7MT (DN26) Contest Paths

*V20 model predictions for the current solar conditions (SFI 116, Kp 2.33).
Which bands can work which continents right now?*

| Destination | 10m | 15m | 20m | 40m |
|-------------|-----|-----|-----|-----|
| Europe (JN48) | CW | CW | CW | CW |
| Japan (PM95) | CW | CW | CW | CW |
| S. America (GG87) | CW | CW | CW | CW |
| Africa (KG33) | FT8 | FT8 | FT8 | FT8 |
| Oceania (QF56) | FT8 | FT8 | FT8 | FT8 |
| Caribbean (FK68) | CW | CW | CW | CW |

*Mode thresholds: SSB &ge; +3 dB, RTTY &ge; -5 dB, CW &ge; -15 dB, FT8 &ge; -21 dB, WSPR &ge; -28 dB.
Predictions update every 3 hours with current solar conditions.*

---

## About This Site

Ham Stats is generated every 3 hours from a self-hosted ClickHouse database
containing **13+ billion** amateur radio propagation observations — the largest
curated dataset of its kind on Earth. No cloud services. No third-party APIs.
Every query runs against data we collected and maintain.

The data comes from four independent networks, each measuring a different layer
of HF propagation:

- **WSPR** (10.92B spots, 2008–present) — the SNR floor at minimum power
- **Reverse Beacon Network** (2.25B spots, 2009–present) — CW/RTTY measured signals
- **PSK Reporter** (356.2M spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234.3M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*