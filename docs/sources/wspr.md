# WSPR — Weak Signal Propagation Reporter

WSPR (pronounced "whisper") uses highly compressed digital transmissions at
roughly 200 mW to probe HF propagation paths. Stations transmit a 2-minute
beacon containing callsign, grid square, and power level. Receiving stations
decode these beacons and report the measured SNR to wsprnet.org.

Because WSPR uses such low power, a decoded spot means the path is open at the
propagation floor — not just open for high-power voice, but open enough to
carry a minimum-power digital signal. This makes it the most sensitive
propagation measurement in the dataset.

**10.8 billion spots. 17 years. The largest amateur radio propagation dataset
on Earth.**

---

## Dataset Statistics

<!-- AUTO-GENERATED: WSPR dataset stats -->

| Metric | Value |
|--------|-------|
| **Total Rows (`wspr.bronze`)** | — |
| **Date Range** | — |
| **Daily Spot Rate (recent 30 days)** | — |
| **Unique Transmitter Callsigns** | — |
| **Unique Receiver Callsigns** | — |
| **Unique Grid Pairs** | — |
| **Bands Covered** | — |

---

## Band Breakdown

<!-- AUTO-GENERATED: WSPR band breakdown -->

| Band | ADIF ID | Spots | Pct of Total |
|------|---------|-------|-------------|
| 160m | 102 | — | — |
| 80m | 103 | — | — |
| 60m | 104 | — | — |
| 40m | 105 | — | — |
| 30m | 106 | — | — |
| 20m | 107 | — | — |
| 17m | 108 | — | — |
| 15m | 109 | — | — |
| 12m | 110 | — | — |
| 10m | 111 | — | — |

*Band IDs are ADIF standard. Band assignment uses frequency-to-band lookup
(single source of truth in `bands.GetBand()`). Fixed as of v2.1.0 re-ingest
(2026-02-03) — all 10.8B rows carry correct ADIF IDs.*

---

## Geographic Coverage

<!-- AUTO-GENERATED: WSPR geographic coverage -->

| Region | Unique Transmitter Grids | Unique Receiver Grids | Unique Grid Pairs |
|--------|-------------------------|----------------------|-------------------|
| North America | — | — | — |
| Europe | — | — | — |
| Asia/Pacific | — | — | — |
| South America | — | — | — |
| Africa | — | — | — |
| Other | — | — | — |

---

## Daily Growth (Last 30 Days)

<!-- AUTO-GENERATED: WSPR daily growth chart -->

| Date | Spots | Cumulative Total |
|------|-------|-----------------|
| — | — | — |
| — | — | — |
| — | — | — |

---

## Data Quality Notes

- SNR range in raw data: -99 to +60 dB. Real WSPR is typically -30 to +20 dB.
- Ground-wave spots (< 500 km) are present in bronze but filtered from
  signatures to focus on ionospheric skip.
- Balloon/telemetry callsigns removed: 1,443 entries identified in
  `wspr.balloon_callsigns_v2`, covering ~950K spots (0.009% of bronze).
- 93.3M rows promoted to `wspr.signatures_v2_terrestrial` after quality
  filtering and solar joining.
