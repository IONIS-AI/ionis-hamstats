---
description: >-
  How Ham Stats transforms raw radio spots into propagation intelligence. From
  WSPR/RBN/PSKR ingestion through ClickHouse aggregation to IONIS neural network
  predictions — the full data pipeline explained.
---

# Methodology

How raw spots become propagation intelligence. This section describes the
pipeline from ingested observations to the signatures and statistics published
on this site.

The short version: 13+ billion raw spots go in, 156+ million quality-filtered,
solar-joined signatures come out. Every number on this site traces back to
a specific query against that corpus.

---

## Bronze → Silver → Gold

| Layer | Table(s) | Rows | Content |
|-------|---------|------|---------|
| Bronze | `wspr.bronze`, `rbn.bronze`, `contest.bronze`, `pskr.bronze` | 13.18B+ | Raw ingested spots, minimal transformation |
| Silver | `wspr.silver` | 4.4B | Float4 embeddings from CUDA signature engine |
| Gold | `wspr.signatures_v2_terrestrial`, `rbn.signatures`, `contest.signatures` | 156.4M | Quality-filtered, solar-joined, ground-wave excluded |

*Solar data: `solar.bronze` (GFZ Potsdam, 2000–present, ~1-day lag) for
historical training; `wspr.live_conditions` (NOAA SWPC, 15-min updates) for
current-conditions reporting.*

---

## The Pipeline

```
Raw Spots (bronze)
    ↓
  Quality Filter (balloon removal, ground-wave filter, AGC outliers)
    ↓
  Solar Join (SFI, Kp, SSN at 3-hour resolution)
    ↓
  Grid Resolution (callsign → Maidenhead grid via callsign_grid)
    ↓
Signatures (silver / gold)
    ↓
  Aggregation (by band, path, time window)
    ↓
Published Reports (this site)
```

Each step is deterministic and reproducible from the raw data. Nothing is
estimated or interpolated except the Maidenhead grid-to-latitude/longitude
conversion for distance calculations.

---

## Pages

- [**Signatures**](signatures.md) — What a signature is: aggregated float4
  vectors combining geography, time, frequency, and solar context. How 10.8B
  raw spots become 93.3M signatures.
- [**Data Quality**](data-quality.md) — What gets filtered and why: balloon
  callsigns, ground-wave spots, RBN AGC outliers, grid normalization.
