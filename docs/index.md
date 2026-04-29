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

![SFI](https://img.shields.io/badge/SFI_145-Elevated-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_0.0-Quiet-teal?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Quiet_+_Radio_Blackout-teal?style=flat-square)

*Updated 21:00 UTC · NOAA SWPC*

---

## Band Activity (Last 24 Hours)

*Which bands had propagation in the last 24 hours, based on spots from all sources.
RBN archives lag ~24 hours; zeroes indicate no data in the window, not band closure.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | 26,436 | 1,847 | 1.1M | +81 dB | Strong |
| 12m | 15,499 | 379 | 1.4M | +56 dB | Strong |
| 15m | 64,098 | 2,258 | 7.2M | +70 dB | Strong |
| 17m | 78,836 | 4,478 | 4.6M | +183 dB | Strong |
| 20m | 327,700 | 16,587 | 12.6M | +170 dB | Strong |
| 30m | 148,121 | 2,986 | 2.7M | +97 dB | Strong |
| 40m | 268,394 | 10,591 | 4.7M | +84 dB | Strong |
| 80m | 69,026 | 1,958 | 574,767 | +57 dB | Strong |
| 160m | 12,898 | 323 | 42,109 | +52 dB | Strong |

---

## Data Pipeline

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-04-28 | 11.34B | Current |
| RBN | 2026-04-28 | 2.30B | Current |
| PSK Reporter | 2026-04-29 | 2.61B | Live |
| Contest | Archive | 234.3M | Static |
| Solar | 2026-04-28 | 77,152 | Current |

---

## About This Site

Ham Stats is generated every 3 hours from a self-hosted ClickHouse database
containing **14+ billion** amateur radio propagation observations — one of the
largest curated datasets of its kind. No cloud services. No third-party APIs.
Every query runs against data we collected and maintain.

The data comes from four independent networks, each measuring a different layer
of HF propagation:

- **WSPR** (11.34B spots, 2008–present) — the SNR floor at minimum power
- **Reverse Beacon Network** (2.30B spots, 2009–present) — CW/RTTY measured signals
- **PSK Reporter** (2.61B spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234.3M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*