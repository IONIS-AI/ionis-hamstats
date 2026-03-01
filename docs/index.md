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
neural network trained on the largest curated amateur radio propagation dataset on Earth.
For technical details on the model and methodology, see
[ionis-ai.com](https://ionis-ai.com/).

![SFI](https://img.shields.io/badge/SFI_147-Elevated-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_1.0-Quiet-teal?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Quiet-teal?style=flat-square)

*Updated 21:00 UTC · NOAA SWPC*

---

## What Can You Work Right Now?

??? info "How do these predictions work?"

    IONIS predicts the **ionospheric SNR floor** for a given path — it has no concept
    of your station, antenna, power, or receiver. It answers one question:
    *"Can the ionosphere support this path right now, and how much signal can it carry?"*

    The model considers five things:

    - **Where** are the two grid squares? (distance, azimuth, latitude, midpoint)
    - **When** is it? (hour of day, season, day/night geometry)
    - **What frequency?**
    - **What's the sun doing?** (Solar Flux Index &rarr; MUF lift)
    - **What's the magnetosphere doing?** (Kp index &rarr; storm penalty)

    From these inputs, the model outputs a predicted SNR in dB. That value is then
    matched against the minimum decode thresholds for each mode — SSB needs a
    strong signal (+3 dB), while WSPR can pull signals out of the noise floor (-28 dB).

    The model was trained on 14+ billion observations across thousands of stations
    with varying power levels and antennas. Because TX power is not a model input,
    these station differences become noise that the model averages over — what it
    learned is the ionosphere itself, not any particular operator's setup.

    The predictions represent a typical path — your actual results will vary with
    your antenna and power, but the path is either open or it isn't.

*IONIS predictions from KI7MT (DN13) for the current solar conditions (SFI 147, Kp 1.0).*

| Destination | 10m | 12m | 15m | 17m | 20m | 30m | 40m | 60m | 80m | 160m |
|-------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Europe (JN48) | RTTY | RTTY | RTTY | RTTY | RTTY | RTTY | SSB | SSB | — | — |
| Japan (PM95) | RTTY | RTTY | RTTY | RTTY | RTTY | RTTY | RTTY | RTTY | — | — |
| S. America (GG87) | RTTY | RTTY | RTTY | RTTY | RTTY | CW | — | — | — | — |
| Africa (KG33) | CW | CW | CW | CW | CW | CW | CW | CW | — | — |
| Oceania (QF56) | RTTY | CW | CW | CW | CW | CW | — | — | — | — |
| Caribbean (FK68) | RTTY | RTTY | RTTY | CW | CW | CW | — | — | — | — |

*Mode thresholds: SSB &ge; +3 dB, RTTY &ge; -5 dB, CW &ge; -15 dB, FT8 &ge; -21 dB, WSPR &ge; -28 dB.
Predictions update every 3 hours with current solar conditions.*

---

## Band Activity (Last 24 Hours)

*Which bands had propagation in the last 24 hours, based on spots from all sources.
RBN archives lag ~24 hours; zeroes indicate no data in the window, not band closure.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | 63,289 | 8,225 | 7.5M | +87 dB | Strong |
| 12m | 27,318 | 738 | 4.6M | +59 dB | Strong |
| 15m | 78,159 | 10,061 | 4.7M | +87 dB | Strong |
| 17m | 67,445 | 1,954 | 2.3M | +87 dB | Strong |
| 20m | 283,129 | 32,075 | 8.5M | +87 dB | Strong |
| 30m | 112,727 | 3,183 | 2.2M | +69 dB | Strong |
| 40m | 160,704 | 33,519 | 6.7M | +87 dB | Strong |
| 80m | 73,966 | 63,734 | 1.3M | +76 dB | Strong |
| 160m | 18,639 | 340 | 193,800 | +53 dB | Strong |

---

## Data Pipeline

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-02-28 | 10.98B | Current |
| RBN | 2026-02-28 | 2.27B | Current |
| PSK Reporter | 2026-03-01 | 670.1M | Live |
| Contest | Archive | 234.3M | Static |
| Solar | 2026-03-01 | 76,698 | Live |

---

## About This Site

Ham Stats is generated every 3 hours from a self-hosted ClickHouse database
containing **14+ billion** amateur radio propagation observations — one of the
largest curated datasets of its kind. No cloud services. No third-party APIs.
Every query runs against data we collected and maintain.

The data comes from four independent networks, each measuring a different layer
of HF propagation:

- **WSPR** (10.98B spots, 2008–present) — the SNR floor at minimum power
- **Reverse Beacon Network** (2.27B spots, 2009–present) — CW/RTTY measured signals
- **PSK Reporter** (670.1M spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234.3M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*