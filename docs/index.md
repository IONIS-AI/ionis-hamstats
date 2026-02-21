# Ham Stats

**HF propagation predictions trained on 13 billion real observations — not theory, not opinions.**

![SFI](https://img.shields.io/badge/SFI_111-Moderate-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_2.0-Quiet-teal?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Quiet-teal?style=flat-square)

*Updated 13:00 UTC · NOAA SWPC*

---

## What Can You Work Right Now?

*IONIS V20 predictions from KI7MT (DN13) for the current solar conditions (SFI 111, Kp 2.0).*

| Destination | 10m | 15m | 20m | 40m | 80m | 160m |
|-------------|-----|-----|-----|-----|-----|------|
| Europe (JN48) | CW | CW | CW | CW | CW | CW |
| Japan (PM95) | CW | CW | CW | CW | CW | CW |
| S. America (GG87) | CW | CW | CW | CW | CW | CW |
| Africa (KG33) | FT8 | FT8 | FT8 | FT8 | FT8 | FT8 |
| Oceania (QF56) | CW | CW | CW | CW | CW | CW |
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
| 10m | 231,165 | 0 | 5.4M | +103 dB | Strong |
| 12m | 114,521 | 0 | 1.7M | +56 dB | Strong |
| 15m | 295,763 | 0 | 4.0M | +66 dB | Strong |
| 17m | 278,138 | 0 | 1.7M | +62 dB | Strong |
| 20m | 1.2M | 0 | 7.7M | +80 dB | Strong |
| 30m | 565,119 | 0 | 2.4M | +72 dB | Strong |
| 40m | 827,499 | 0 | 7.8M | +80 dB | Strong |
| 80m | 212,382 | 0 | 2.1M | +65 dB | Strong |
| 160m | 62,705 | 0 | 379,745 | +67 dB | Strong |

---

## Data Pipeline

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-02-20 | 10.92B | Current |
| RBN | 2026-02-19 | 2.25B | 2 days behind |
| PSK Reporter | 2026-02-21 | 377.4M | Live |
| Contest | Archive | 234.3M | Static |
| Solar | 2026-02-21 | 76,628 | Live |

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
- **PSK Reporter** (377.4M spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234.3M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*