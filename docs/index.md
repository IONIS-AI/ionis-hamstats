---
description: >-
  Live HF band conditions and IONIS propagation predictions updated every 3 hours.
  Current solar flux, Kp index, band activity from WSPR, RBN, and PSK Reporter,
  and AI-powered predictions for 6 global destinations.
---

# Ham Stats

**HF propagation predictions trained on 14 billion real observations — not theory, not opinions.**

Ham Stats provides live HF propagation intelligence for amateur radio operators.
Everything on this site is derived from measured radio observations — WSPR beacons,
Reverse Beacon Network skimmers, PSK Reporter reception reports, and contest
QSOs — combined with real-time solar conditions from NOAA.

- **Predictions** — Which bands and modes can reach your target right now
- **Band Activity** — What's actually being heard across the HF spectrum
- **Solar Conditions** — Current SFI, Kp, and their impact on propagation
- **Historical Data** — Band-by-band trends, contest schedules, and DXpedition tracking

The predictions are powered by [IONIS](https://ionis-ai.com/) — a physics-constrained
neural network trained on one of the largest curated amateur radio propagation datasets we are aware of.
For technical details on the model and methodology, see
[ionis-ai.com](https://ionis-ai.com/).

![SFI](https://img.shields.io/badge/SFI_106-Moderate-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_0.67-Quiet-teal?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Quiet-teal?style=flat-square)

*Updated 21:00 UTC · NOAA SWPC*

---

## Band Activity (Last 24 Hours)

*Which bands had propagation in the last 24 hours, based on spots from all sources.
RBN archives lag ~24 hours; zeroes indicate no data in the window, not band closure.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | 54,454 | 4,316 | 2.4M | +86 dB | Strong |
| 12m | 20,915 | 316 | 961,625 | +55 dB | Strong |
| 15m | 67,335 | 3,007 | 4.8M | +87 dB | Strong |
| 17m | 57,980 | 1,751 | 2.6M | +174 dB | Strong |
| 20m | 274,821 | 9,968 | 10.4M | +87 dB | Strong |
| 30m | 115,994 | 3,645 | 2.9M | +60 dB | Strong |
| 40m | 190,245 | 10,988 | 7.0M | +87 dB | Strong |
| 80m | 66,158 | 2,773 | 1.1M | +87 dB | Strong |
| 160m | 15,726 | 305 | 91,010 | +50 dB | Strong |

---

## Data Pipeline

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-03-18 | 11.10B | Current |
| RBN | 2026-03-18 | 2.27B | Current |
| PSK Reporter | 2026-03-19 | 1.32B | Live |
| Contest | Archive | 234.3M | Static |
| Solar | 2026-03-19 | 76,842 | Live |

---

## About This Site

Ham Stats is generated every 3 hours from a self-hosted ClickHouse database
containing **14+ billion** amateur radio propagation observations — one of the
largest curated datasets of its kind. No cloud services. No third-party APIs.
Every query runs against data we collected and maintain.

The data comes from four independent networks, each measuring a different layer
of HF propagation:

- **WSPR** (11.10B spots, 2008–present) — the SNR floor at minimum power
- **Reverse Beacon Network** (2.27B spots, 2009–present) — CW/RTTY measured signals
- **PSK Reporter** (1.32B spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234.3M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*