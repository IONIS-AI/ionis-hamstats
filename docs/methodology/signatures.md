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

The gold tables (`wspr.signatures_v2_terrestrial`, `rbn.signatures`,
`contest.signatures`, `pskr.signatures`) hold the filtered subset used for training and
reporting. They are built from the bronze tables directly.

---

## How 12.7B Spots Become 93.6M Signatures

**Step 1 — Bronze ingest.** Raw CSV rows from wsprnet.org archives are loaded
into `wspr.bronze`. All 12.7B rows, including noise, duplicates, and edge
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
| `wspr.signatures_v2_terrestrial` | 93.6M | -28 to +20 dB | WSPR |
| `rbn.signatures` | 56.7M | -20 to 80 dB (filtered) | RBN |
| `contest.signatures` | 6.3M | +10/0 dB (anchored) | Contest |

These three tables are UNION ALL compatible — same schema, same solar join,
same grid encoding.

---

## The Float4 Embedding — retired

The CUDA signature engine (`ionis-cuda`) encodes each signature as a float4 vector for fast
similarity search: geography, time, solar and frequency features, normalized to the same scale
as the IONIS training features.

**It is not part of the pipeline and nothing on this site derives from it.** Its destination
table, `wspr.silver`, was found holding zero rows and dropped on 2026-09-22 — the engine is
unpackaged and hand-run, and no report, signature table or training set ever read its output.
Every number published here comes from the signatures tables above, which are built from
`wspr.bronze` directly.

Lineage for every table in the lab:
[`ionis-core/docs/DATA-DICTIONARY.md`](https://github.com/IONIS-AI/ionis-core/blob/main/docs/DATA-DICTIONARY.md)
