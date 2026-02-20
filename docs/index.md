# Ham Stats

**HF propagation predictions trained on 13 billion real observations — not theory, not opinions.**

![SFI](https://img.shields.io/badge/SFI_111-Moderate-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_2.67-Quiet-teal?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Quiet-teal?style=flat-square)

*Updated 23:52 UTC · NOAA SWPC*

---

## What Can You Work Right Now?

*IONIS V20 predictions from KI7MT (DN13) for the current solar conditions (SFI 111, Kp 2.67).*

| Destination | 10m | 15m | 20m | 40m | 80m | 160m |
|-------------|-----|-----|-----|-----|-----|------|
| Europe (JN48) | CW | CW | CW | CW | CW | CW |
| Japan (PM95) | CW | CW | CW | CW | CW | CW |
| S. America (GG87) | FT8 | FT8 | FT8 | FT8 | FT8 | FT8 |
| Africa (KG33) | WSPR | WSPR | WSPR | WSPR | WSPR | WSPR |
| Oceania (QF56) | FT8 | FT8 | FT8 | WSPR | WSPR | WSPR |
| Caribbean (FK68) | CW | CW | CW | CW | CW | CW |

*Mode thresholds: SSB &ge; +3 dB, RTTY &ge; -5 dB, CW &ge; -15 dB, FT8 &ge; -21 dB, WSPR &ge; -28 dB.
Predictions update every 3 hours with current solar conditions.*

**Want predictions from your grid?** Custom prediction tool coming soon — enter your grid and get personalized band/mode forecasts.

---

## Band Activity (Last 24 Hours)

*Which bands had propagation in the last 24 hours, based on spots from all sources.
RBN archives lag ~24 hours; zeroes indicate no data in the window, not band closure.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | 1,109 | 99 | 5.7M | +103 dB | Strong |
| 12m | 720 | 4 | 1.6M | +59 dB | Strong |
| 15m | 2,145 | 245 | 4.0M | +87 dB | Strong |
| 17m | 1,658 | 54 | 1.7M | +62 dB | Strong |
| 20m | 7,311 | 405 | 7.7M | +80 dB | Strong |
| 30m | 3,798 | 39 | 2.2M | +57 dB | Strong |
| 40m | 5,902 | 430 | 7.3M | +86 dB | Strong |
| 80m | 3,060 | 242 | 1.9M | +87 dB | Strong |
| 160m | 838 | 0 | 282,601 | +58 dB | Strong |

---

## Data Pipeline

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-02-19 | 10.92B | Current |
| RBN | 2026-02-19 | 2.25B | Current |
| PSK Reporter | 2026-02-20 | 361.3M | Live |
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
- **PSK Reporter** (361.3M spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234.3M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*