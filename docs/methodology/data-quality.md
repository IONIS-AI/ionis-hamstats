# Data Quality

The raw data has problems. All of it. Balloon telemetry masquerading as
amateur stations. SDR AGC artifacts reporting 233 dB signals. Ground-wave
contacts at 5 km that have nothing to do with ionospheric propagation. Grid
squares stored as FixedString(8) with null-byte padding.

This page documents every filter applied and why. Every filter has a
measurable effect on the dataset. Numbers below reflect the state of the
gold-layer signature tables.

---

## Filter 1 — Balloon and Telemetry Callsigns (WSPR)

**Problem:** A subset of WSPR callsigns are not amateur stations — they are
balloon telemetry payloads transmitting on amateur frequencies. These spots
represent the balloon's position, not a propagation path between fixed
stations. Including them corrupts geographic coverage statistics and any
path-based model.

**Solution:** `wspr.balloon_callsigns_v2` maintains a list of known balloon
callsigns identified via date-level velocity flagging (stations that move
faster than physically possible for a fixed station). The v2 table includes
the full Rosetta Stone cross-reference.

| Metric | Value |
|--------|-------|
| Balloon callsigns identified | 1,443 |
| Spots removed | ~950,000 |
| Pct of bronze removed | 0.009% |
| Detection method | Date-level velocity flags + Rosetta Stone |

*The assertion: `populate_callsign_grid.sh` enforces a 3M minimum row check
after balloon removal to confirm the filter is not over-aggressive.*

---

## Filter 2 — Ground-Wave Exclusion (WSPR)

**Problem:** Spots at distances under 500 km are often ground-wave, not
ionospheric skip. Ground-wave propagation is distance-limited and not subject
to the same solar forcing as ionospheric paths. Including short-path spots
dilutes the ionospheric signal in the data.

**Solution:** All spots where the great-circle distance between TX grid center
and RX grid center is less than 500 km are excluded from signatures. They
remain in `wspr.bronze`.

| Metric | Value |
|--------|-------|
| Distance threshold | 500 km |
| Spots excluded (est.) | — |
| Tables affected | `wspr.signatures_v2_terrestrial` |

---

## Filter 3 — RBN AGC Outlier Filtering

**Problem:** RBN skimmer receivers use automatic gain control that can
saturate under strong local signals, reporting absurd SNR values. Raw RBN
data contains spots up to 233 dB — physically impossible for HF propagation.

**Solution:** `rbn.signatures` filters to SNR range -20 to 80 dB. Values
outside this range are excluded from signatures. They remain in `rbn.bronze`.

| Metric | Value |
|--------|-------|
| Raw SNR range observed | up to 233 dB |
| Filter range applied | -20 to 80 dB |
| Spots excluded (est.) | — |
| Tables affected | `rbn.signatures` |

---

## Filter 4 — FixedString Null-Byte Stripping (ClickHouse)

**Problem:** ClickHouse stores grid squares as `FixedString(8)`, which
right-pads shorter values with null bytes (`\0`). A 4-character grid like
`EN52` is stored as `EN52\0\0\0\0`. When used in string comparisons,
joins, or output, the null bytes cause mismatches.

**Solution:** Grid values are stripped of trailing null bytes before any
join, comparison, or output. The pattern `trimRight(grid, '\0')` is applied
consistently throughout population scripts and reporting queries.

**Also:** Grid squares are validated against the Maidenhead format regex
(`[A-R]{2}[0-9]{2}` for 4-character) before being written to signature
tables. Malformed grids (empty, wrong length, non-standard characters) are
excluded.

---

## Filter 5 — Solar Data Gaps

**Problem:** `solar.bronze` has gaps. The GFZ Potsdam archive is continuous
from 2000 onward but may have short gaps from download failures or source
outages. Spots that fall in a solar data gap have no SFI, Kp, or SSN to
join.

**Solution:** Solar fields for gap-affected spots are coalesced to 0 in
signatures. This is flagged in the signature row. Gap spans are tracked in
pipeline logs.

*Note: The solar backfill covers 2000–2026. Gaps prior to 2000 mean WSPR
spots from 2008 onward are fully covered for Kp, but SFI and SSN may have
short gaps where the Potsdam download failed.*

---

## Filter 6 — SNR Clipping (WSPR)

**Problem:** Raw WSPR SNR ranges from -99 to +60 dB. Real WSPR propagation
is typically -30 to +20 dB. Values outside this range indicate receiver
overload, decode errors, or software bugs.

**Solution:** In reporting and model training, SNR is soft-clipped. The
signature tables include the raw median SNR; clipping is applied at the
query or training layer depending on the use case.

| Metric | Value |
|--------|-------|
| Raw SNR range | -99 to +60 dB |
| Typical WSPR range | -30 to +20 dB |
| Clipping strategy | Query-layer; not applied in bronze |

---

## Summary

| Filter | Source | Rows Removed | Effect |
|--------|--------|-------------|--------|
| Balloon callsigns | WSPR | ~950K | Removes telemetry from path stats |
| Ground-wave (< 500 km) | WSPR | — | Focuses on ionospheric skip |
| AGC outliers | RBN | — | Removes physically impossible SNR |
| FixedString null bytes | All | 0 (normalization, not removal) | Enables correct joins |
| Solar data gaps | All | 0 (zeroed, not removed) | Flags incomplete solar context |
