---
description: >-
  Measured SNR degradation during geomagnetic storms from actual WSPR observations.
  Before/during/after comparison by band, storm recovery timelines, and historical
  storm frequency across Solar Cycle 25.
---

# Storm Impact Analysis

*Updated 12:00 UTC 2026-02-27*

This page shows measured SNR degradation during geomagnetic storms. All values
come from actual WSPR signal measurements joined against Kp index at daily
resolution.

A geomagnetic storm is defined here as Kp >= 5 (NOAA G1 or above). Consecutive
storm days are merged into a single event. SNR before/during/after is the median
across all recorded WSPR spots on each band during the respective window,
filtered to ionospheric paths (> 500 km).

---

## Recent Storm Events

| Storm Date (UTC) | Peak Kp | Classification |
|------------------|---------|----------------|
| 2026-02-22 | 5.33 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2026-01-11 | 5.33 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2026-01-10 | 5.67 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2026-01-02 | 5.0 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2025-12-12 | 5.0 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2025-12-11 | 6.0 | ![G2 Moderate](https://img.shields.io/badge/G2_Moderate-orange?style=flat-square) |
| 2025-12-10 | 6.0 | ![G2 Moderate](https://img.shields.io/badge/G2_Moderate-orange?style=flat-square) |
| 2025-12-04 | 5.0 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2025-12-03 | 6.67 | ![G2 Moderate](https://img.shields.io/badge/G2_Moderate-orange?style=flat-square) |
| 2025-11-13 | 7.33 | ![G3 Strong](https://img.shields.io/badge/G3_Strong-red?style=flat-square) |
| 2025-11-12 | 8.67 | ![G4 Severe](https://img.shields.io/badge/G4_Severe-red?style=flat-square) |
| 2025-11-08 | 6.0 | ![G2 Moderate](https://img.shields.io/badge/G2_Moderate-orange?style=flat-square) |
| 2025-11-07 | 5.33 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2025-11-06 | 6.67 | ![G2 Moderate](https://img.shields.io/badge/G2_Moderate-orange?style=flat-square) |
| 2025-11-05 | 5.67 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2025-10-30 | 5.33 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2025-10-19 | 5.0 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2025-10-18 | 6.33 | ![G2 Moderate](https://img.shields.io/badge/G2_Moderate-orange?style=flat-square) |
| 2025-10-12 | 5.0 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
| 2025-10-03 | 5.0 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |

---

## SNR Before / During / After — Storm of 2026-02-22 (Kp 5.33)

*Median WSPR SNR (dB) on ionospheric paths (> 500 km) for the day before,
day of, and day after peak Kp.*

| Band | Before (dB) | During (dB) | After (dB) | Change | Recovery vs Baseline |
|------|------------|-------------|-----------|--------|---------------------|
| 10m | -18 | -18 | -18 | 0 dB | 0 dB |
| 15m | -18 | -18 | -18 | 0 dB | 0 dB |
| 20m | -15 | -15 | -15 | 0 dB | 0 dB |
| 40m | -17 | -16 | -17 | +1 dB | 0 dB |
| 80m | -18 | -18 | -18 | 0 dB | 0 dB |
| 160m | -18 | -18 | -18 | 0 dB | 0 dB |

*Change = During − Before (negative = degradation). Recovery vs Baseline =
After − Before (0 = full recovery, negative = still degraded).*

---

## Recovery Timeline

Hours after storm end until median WSPR SNR returns to within 1 dB of
pre-storm baseline, by band. Aggregated across all storms (Kp >= 5) in
the last 2 years. Consecutive storm days are merged into single events.

| Band | Median Recovery (hrs) | 90th Percentile (hrs) | Storm Count |
|------|----------------------|----------------------|-------------|
| 10m | 24 | 24 | 60 |
| 15m | 24 | 24 | 60 |
| 20m | 24 | 24 | 60 |
| 40m | 24 | 48 | 60 |
| 80m | 24 | 24 | 58 |
| 160m | 24 | 48 | 60 |

*Recovery = first day post-storm where band median SNR is within 1 dB of the
day before the storm. Reported in hours (days × 24). Storms where SNR did not
recover within 7 days are excluded.*

---

## Storm Frequency by Year

| Year | Kp>=5 Days | Kp>=7 Days | Peak Kp | Cycle Phase |
|------|-----------|-----------|---------|-------------|
| 2026 | 4 | 0 | 5.7 | Active |
| 2025 | 62 | 8 | 8.7 | Maximum |
| 2024 | 36 | 13 | 9.0 | Maximum |
| 2023 | 41 | 5 | 8.3 | Maximum |
| 2022 | 36 | 0 | 6.7 | Active |
| 2021 | 17 | 2 | 7.7 | Moderate |
| 2020 | 3 | 0 | 5.7 | Minimum |
| 2019 | 12 | 0 | 6.3 | Minimum |
| 2018 | 13 | 1 | 7.3 | Minimum |
| 2017 | 37 | 3 | 8.3 | Moderate |
| 2016 | 43 | 0 | 6.3 | Moderate |
| 2015 | 56 | 6 | 8.3 | Active |
| 2014 | 12 | 0 | 6.3 | Active |
| 2013 | 23 | 2 | 7.7 | Active |
| 2012 | 35 | 2 | 8.0 | Active |
| 2011 | 26 | 3 | 7.7 | Active |
| 2010 | 11 | 1 | 7.7 | Moderate |
| 2009 | 3 | 0 | 5.7 | Minimum |
| 2008 | 11 | 0 | 6.3 | Minimum |
| 2007 | 19 | 0 | 5.7 | Minimum |
| 2006 | 28 | 3 | 8.3 | Moderate |
| 2005 | 55 | 15 | 8.7 | Moderate |
| 2004 | 41 | 10 | 8.7 | Active |
| 2003 | 120 | 10 | 9.0 | Active |
| 2002 | 50 | 9 | 8.3 | Maximum |
| 2001 | 50 | 14 | 8.7 | Maximum |
| 2000 | 67 | 14 | 9.0 | Maximum |

*Storm counts from `solar.bronze` (GFZ Potsdam historical data, backfilled
2000–present). Each row counts the number of days in that year where the
daily peak Kp reached the indicated threshold.*