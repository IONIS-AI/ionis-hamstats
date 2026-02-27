# WSPR — Weak Signal Propagation Reporter

WSPR (pronounced "whisper") uses highly compressed digital transmissions at
roughly 200 mW to probe HF propagation paths. Stations transmit a 2-minute
beacon containing callsign, grid square, and power level. Receiving stations
decode these beacons and report the measured SNR to wsprnet.org.

Because WSPR uses such low power, a decoded spot means the path is open at the
propagation floor — not just open for high-power voice, but open enough to
carry a minimum-power digital signal. This makes it the most sensitive
propagation measurement in the dataset.

**10.96B spots. 18 years. One of the largest amateur radio propagation
datasets of its kind.**

---

## Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Rows (`wspr.bronze`)** | 10.96B |
| **Date Range** | 2008-03-11 to 2026-02-25 |
| **Daily Spot Rate (recent)** | ~7M spots/day |
| **Unique Transmitter Callsigns** | 3.6M |
| **Unique Receiver Callsigns** | 99,335 |
| **Unique Grid Pairs** | 8.3M |
| **Bands Covered** | 160m–10m (10 HF bands) |

---

## Band Breakdown

| Band | ADIF ID | Spots | Pct of Total |
|------|---------|-------|-------------|
| 160m | 102 | 192.7M | 1.76% |
| 80m | 103 | 828.5M | 7.56% |
| 60m | 104 | 123.7M | 1.13% |
| 40m | 105 | 3.51B | 32.05% |
| 30m | 106 | 1.84B | 16.82% |
| 20m | 107 | 2.95B | 26.92% |
| 17m | 108 | 408.3M | 3.73% |
| 15m | 109 | 397.5M | 3.63% |
| 12m | 110 | 120.0M | 1.1% |
| 10m | 111 | 324.9M | 2.97% |

*Band IDs are ADIF standard. Band assignment uses frequency-to-band lookup
(single source of truth in `bands.GetBand()`). Fixed as of v2.1.0 re-ingest
(2026-02-03) — all rows carry correct ADIF IDs.*

---

## Data Quality Notes

- SNR range in raw data: -99 to +60 dB. Real WSPR is typically -30 to +20 dB.
- Ground-wave spots (< 500 km) are present in bronze but filtered from
  signatures to focus on ionospheric skip.
- Balloon/telemetry callsigns removed: 1,443 entries identified in
  `wspr.balloon_callsigns_v2`, covering ~950K spots (0.009% of bronze).
- 93.6M rows promoted to `wspr.signatures_v2_terrestrial` after quality
  filtering and solar joining.