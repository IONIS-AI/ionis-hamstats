# Storm Impact Analysis

This page shows measured SNR degradation during geomagnetic storms. All values
come from actual signal measurements — WSPR, RBN, and PSK Reporter spots
collected during storm events — joined against Kp index at 3-hour resolution.

A geomagnetic storm is defined here as Kp >= 5, sustained for at least 3 hours.
SNR before/during/after is the median across all recorded spots on each band
during the respective window.

---

## Recent Storm Events

| Storm Date (UTC) | Peak Kp | Classification |
|------------------|---------|----------------|
| 2026-02-16 | 6.0 | ![G2 Moderate](https://img.shields.io/badge/G2_Moderate-orange?style=flat-square) |
| 2026-02-15 | 5.33 | ![G1 Minor](https://img.shields.io/badge/G1_Minor-orange?style=flat-square) |
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

---

## SNR Before / During / After — Most Recent Storm

*Median SNR (dB) measured from WSPR spots in the 24-hour window before,
during, and 24-hour window after peak Kp.*

| Band | Before (dB) | During (dB) | After (dB) | Change During | Recovery |
|------|------------|-------------|-----------|---------------|----------|
| 10m | — | — | — | — | — |
| 15m | — | — | — | — | — |
| 20m | — | — | — | — | — |
| 40m | — | — | — | — | — |
| 80m | — | — | — | — | — |
| 160m | — | — | — | — | — |

*Coming soon — requires per-storm SNR comparison query.*

---

## Recovery Timeline

Hours after peak Kp until median SNR returns to within 1 dB of pre-storm
baseline, by band. Averaged across all storms in the dataset where Kp >= 5.

| Band | Median Recovery (hrs) | 90th Percentile (hrs) | Storm Count |
|------|----------------------|----------------------|-------------|
| 10m | — | — | — |
| 15m | — | — | — |
| 20m | — | — | — |
| 40m | — | — | — |
| 80m | — | — | — |
| 160m | — | — | — |

*Coming soon — requires recovery analysis query.*

---

## Storm Frequency by Year

| Year | Kp>=5 Events | Kp>=7 Events | Peak Kp | Cycle Phase |
|------|-------------|-------------|---------|-------------|
| — | — | — | — | — |

*Storm counts derived from `solar.bronze` (GFZ Potsdam historical data,
backfilled 2000–2026). Coming soon.*