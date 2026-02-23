---
description: >-
  Live HF band conditions and IONIS propagation predictions updated every 3 hours.
  Current solar flux, Kp index, band activity from WSPR, RBN, and PSK Reporter,
  and AI-powered predictions for 6 global destinations.
---

# Ham Stats

**HF propagation predictions trained on 13 billion real observations — not theory, not opinions.**

![SFI](https://img.shields.io/badge/SFI_108-Moderate-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_4.33-Active-orange?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Unsettled-orange?style=flat-square)

*Updated 22:00 UTC · NOAA SWPC*

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

    The model was trained on 13+ billion WSPR spots across thousands of stations
    with varying power levels and antennas. Because TX power is not a model input,
    these station differences become noise that the model averages over — what it
    learned is the ionosphere itself, not any particular operator's setup.

    The predictions represent a typical path — your actual results will vary with
    your antenna and power, but the path is either open or it isn't.

*IONIS V20 predictions from KI7MT (DN13) for the current solar conditions (SFI 108, Kp 4.33).*

| Destination | 10m | 15m | 20m | 40m | 80m | 160m |
|-------------|-----|-----|-----|-----|-----|------|
| Europe (JN48) | CW | CW | CW | CW | CW | CW |
| Japan (PM95) | CW | CW | CW | CW | CW | FT8 |
| S. America (GG87) | FT8 | FT8 | FT8 | FT8 | FT8 | FT8 |
| Africa (KG33) | WSPR | WSPR | WSPR | WSPR | WSPR | WSPR |
| Oceania (QF56) | WSPR | WSPR | WSPR | WSPR | WSPR | WSPR |
| Caribbean (FK68) | CW | CW | CW | CW | CW | FT8 |

*Mode thresholds: SSB &ge; +3 dB, RTTY &ge; -5 dB, CW &ge; -15 dB, FT8 &ge; -21 dB, WSPR &ge; -28 dB.
Predictions update every 3 hours with current solar conditions.*

**Want predictions from your grid?** Custom prediction tool coming soon — enter your grid and get personalized band/mode forecasts.

---

## Band Activity (Last 24 Hours)

*Which bands had propagation in the last 24 hours, based on spots from all sources.
RBN archives lag ~24 hours; zeroes indicate no data in the window, not band closure.*

| Band | WSPR Spots | RBN Spots | PSKR Spots | Peak SNR | Status |
|------|-----------|-----------|------------|----------|--------|
| 10m | 19,381 | 0 | 3.9M | +104 dB | Strong |
| 12m | 10,295 | 0 | 1.4M | +66 dB | Strong |
| 15m | 32,054 | 0 | 4.5M | +87 dB | Strong |
| 17m | 36,944 | 0 | 2.0M | +78 dB | Strong |
| 20m | 149,357 | 0 | 8.6M | +91 dB | Strong |
| 30m | 68,836 | 0 | 2.2M | +87 dB | Strong |
| 40m | 101,978 | 0 | 6.6M | +69 dB | Strong |
| 80m | 42,340 | 0 | 2.0M | +87 dB | Strong |
| 160m | 14,952 | 0 | 236,291 | +54 dB | Strong |

---

## Data Pipeline

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-02-22 | 10.94B | Current |
| RBN | 2026-02-21 | 2.26B | 2 days behind |
| PSK Reporter | 2026-02-23 | 469.3M | Live |
| Contest | Archive | 234.3M | Static |
| Solar | 2026-02-23 | 76,652 | Live |

---

## About This Site

Ham Stats is generated every 3 hours from a self-hosted ClickHouse database
containing **13+ billion** amateur radio propagation observations — one of the
largest curated datasets of its kind. No cloud services. No third-party APIs.
Every query runs against data we collected and maintain.

The data comes from four independent networks, each measuring a different layer
of HF propagation:

- **WSPR** (10.94B spots, 2008–present) — the SNR floor at minimum power
- **Reverse Beacon Network** (2.26B spots, 2009–present) — CW/RTTY measured signals
- **PSK Reporter** (469.3M spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234.3M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*