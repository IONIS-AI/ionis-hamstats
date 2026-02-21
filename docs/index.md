# Ham Stats

**HF propagation predictions trained on 13 billion real observations — not theory, not opinions.**

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

    The model was trained on 13+ billion WSPR spots where every station transmits
    at the same power (~200 mW) into similar antennas. This controls for the station
    variable — what the model learned is the ionosphere itself, not the operator.

    Any station at the same grid square would see the same propagation physics.
    A bigger antenna or more power shifts *your* results, but the path is either
    open or it isn't.

![SFI](https://img.shields.io/badge/SFI_111-Moderate-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_1.67-Quiet-teal?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Quiet-teal?style=flat-square)

*Updated 18:31 UTC · NOAA SWPC*

---

## What Can You Work Right Now?

*IONIS V20 predictions from KI7MT (DN13) for the current solar conditions (SFI 111, Kp 1.67).*

| Destination | 10m | 15m | 20m | 40m | 80m | 160m |
|-------------|-----|-----|-----|-----|-----|------|
| Europe (JN48) | CW | CW | CW | CW | CW | CW |
| Japan (PM95) | CW | CW | CW | CW | CW | CW |
| S. America (GG87) | CW | CW | CW | CW | CW | CW |
| Africa (KG33) | FT8 | FT8 | FT8 | FT8 | FT8 | FT8 |
| Oceania (QF56) | FT8 | FT8 | FT8 | FT8 | FT8 | FT8 |
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
| 10m | 96,536 | 0 | 4.6M | +103 dB | Strong |
| 12m | 58,530 | 0 | 1.5M | +87 dB | Strong |
| 15m | 143,172 | 0 | 4.1M | +66 dB | Strong |
| 17m | 132,174 | 0 | 1.8M | +87 dB | Strong |
| 20m | 515,138 | 0 | 8.2M | +95 dB | Strong |
| 30m | 216,319 | 0 | 2.3M | +72 dB | Strong |
| 40m | 331,256 | 0 | 8.2M | +80 dB | Strong |
| 80m | 137,777 | 0 | 2.1M | +76 dB | Strong |
| 160m | 46,818 | 0 | 384,804 | +67 dB | Strong |

---

## Data Pipeline

| Source | Latest Date | Total Rows | Status |
|--------|------------|------------|--------|
| WSPR | 2026-02-20 | 10.92B | Current |
| RBN | 2026-02-19 | 2.25B | 2 days behind |
| PSK Reporter | 2026-02-21 | 388.9M | Live |
| Contest | Archive | 234.3M | Static |
| Solar | 2026-02-21 | 76,632 | Live |

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
- **PSK Reporter** (388.9M spots, live since Feb 2026) — FT8/digital operational contacts
- **Contest Logs** (234.3M QSOs, 2005–present) — the SSB/RTTY ceiling at contest power

Solar indices (SFI, Kp, SSN) are joined at 3-hour resolution so every
propagation measurement has its solar context.

This site is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System.

*The logs were speaking for decades, but nobody was listening. Now we're
listening — and we're publishing what we hear.*