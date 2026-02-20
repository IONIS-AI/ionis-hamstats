# Signatures

A signature is a single aggregated propagation measurement for a specific
transmitter–receiver path, band, and 3-hour time window, with solar conditions
attached. It is the unit of analysis that sits between a raw spot and a
training example.

Raw spots are noisy. A single WSPR decode can be affected by local RFI,
equipment quirks, or transient ionospheric conditions. Aggregating multiple
spots from the same path and time window gives a more stable measurement.
A signature is that aggregated result.

---

## What Goes Into a Signature

Each signature encodes:

| Feature | Source | Notes |
|---------|--------|-------|
| TX grid (Maidenhead 4-char) | `wspr.callsign_grid` | Resolved from callsign |
| RX grid (Maidenhead 4-char) | `wspr.callsign_grid` | Resolved from callsign |
| Path distance (km) | Computed | Great-circle from grid centers |
| TX latitude / longitude | Computed | From Maidenhead grid |
| RX latitude / longitude | Computed | From Maidenhead grid |
| Band (ADIF ID) | `wspr.bronze` | Normalized; fixed as of v2.1.0 |
| Median SNR (dB) | `wspr.bronze` | Aggregated over 3-hr window |
| Spot count | `wspr.bronze` | Number of spots in window |
| Hour of day (UTC) | `wspr.bronze` | 3-hour bucket midpoint |
| Day of year | `wspr.bronze` | Seasonal position |
| SFI | `solar.bronze` | 3-hr bucket join |
| Kp | `solar.bronze` | 3-hr bucket join (`intDiv(toHour(ts),3)`) |
| SSN | `solar.bronze` | 3-hr bucket join |

The CUDA signature engine (ionis-cuda) encodes these as float4 vectors stored
in `wspr.silver`. Signatures in the gold tables (`wspr.signatures_v2_terrestrial`,
`rbn.signatures`, `contest.signatures`) are the filtered subset used for
training and reporting.

---

## How 10.8B Spots Become 93.3M Signatures

**Step 1 — Bronze ingest.** Raw CSV rows from wsprnet.org archives are loaded
into `wspr.bronze`. All 10.8B rows, including noise, duplicates, and edge
cases.

**Step 2 — Quality filtering.** Balloon callsigns removed. Spots < 500 km
excluded (ground-wave, not ionospheric). SNR clipped to real WSPR range.
See [Data Quality](data-quality.md) for the full filter list.

**Step 3 — Callsign grid resolution.** Transmitter and receiver callsigns
are resolved to Maidenhead grid squares via `wspr.callsign_grid`. Callsigns
without a resolvable grid are excluded.

**Step 4 — Solar join.** Each spot is joined to `solar.bronze` on
`intDiv(toHour(timestamp), 3)` to attach the 3-hour Kp bucket and daily
SFI/SSN values. Spots with no solar data (gaps in the archive) have solar
fields zeroed.

**Step 5 — Aggregation.** Spots are grouped by (tx_grid, rx_grid, band,
3-hr bucket, date). Median SNR, spot count, and solar indices are computed
per group. The result is one row per unique (path, band, time window).

**Step 6 — Promotion to gold.** Aggregated rows meeting minimum spot count
thresholds are written to the signatures tables.

---

## Signature Table Summary

| Table | Rows | SNR Range | Source |
|-------|------|----------|--------|
| `wspr.signatures_v2_terrestrial` | 93.3M | -28 to +20 dB | WSPR |
| `rbn.signatures` | 56.7M | -20 to 80 dB (filtered) | RBN |
| `contest.signatures` | 6.3M | +10/0 dB (anchored) | Contest |

These three tables are UNION ALL compatible — same schema, same solar join,
same grid encoding.

---

## The Float4 Embedding (wspr.silver)

The CUDA signature engine (ionis-cuda) encodes each signature as a float4
vector for fast similarity search. The engine reads from `wspr.bronze`,
applies the same quality filter and solar join, and writes to `wspr.silver`.

- 4.4B embeddings in `wspr.silver` (41 GiB)
- Generated on RTX PRO 6000 (96 GB) via CUDA bulk processor
- Encoding: geography features + time features + solar features + frequency
  — all normalized to the same scale as the IONIS training features
