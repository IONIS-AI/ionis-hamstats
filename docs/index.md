# Ham Stats

**HF propagation reports generated from real data — not models, not opinions.**

![SFI](https://img.shields.io/badge/SFI_111-Moderate-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_2.33-Quiet-teal?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Quiet-teal?style=flat-square)

*Updated 21:01 UTC · NOAA SWPC*

---

## What Can You Work Right Now?

*IONIS V20 predictions from KI7MT (DN26) for the current solar conditions (SFI 111, Kp 2.33).*

| Destination | 10m | 15m | 20m | 40m |
|-------------|-----|-----|-----|-----|
| Europe (JN48) | CW | CW | CW | CW |
| Japan (PM95) | CW | CW | CW | CW |
| S. America (GG87) | CW | CW | CW | FT8 |
| Africa (KG33) | FT8 | FT8 | FT8 | WSPR |
| Oceania (QF56) | FT8 | FT8 | FT8 | FT8 |
| Caribbean (FK68) | CW | CW | CW | CW |

*Mode thresholds: SSB &ge; +3 dB, RTTY &ge; -5 dB, CW &ge; -15 dB, FT8 &ge; -21 dB, WSPR &ge; -28 dB.
Predictions update every 3 hours with current solar conditions.*

---

## Band Activity (Last 24 Hours)

*Which bands had propagation in the last 24 hours, based on spots from all sources.
RBN archives lag ~24 hours; zeroes indicate no data in the window, not band closure.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | 43,396 | 0 | 5.7M | +61 dB | Strong |
| 12m | 20,674 | 0 | 1.7M | +59 dB | Strong |
| 15m | 63,367 | 0 | 4.1M | +87 dB | Strong |
| 17m | 64,683 | 0 | 1.7M | +62 dB | Strong |
| 20m | 255,284 | 0 | 7.4M | +80 dB | Strong |
| 30m | 108,137 | 0 | 2.1M | +58 dB | Strong |
| 40m | 153,591 | 0 | 7.2M | +86 dB | Strong |
| 80m | 81,564 | 0 | 1.7M | +87 dB | Strong |
| 160m | 22,927 | 0 | 238,008 | +54 dB | Strong |

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

## About This Site

Ham Stats is generated every 3 hours from a self-hosted ClickHouse database
containing **13+ billion** amateur radio propagation observations — one of the
largest curated datasets of its kind. No cloud services. No third-party APIs.
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