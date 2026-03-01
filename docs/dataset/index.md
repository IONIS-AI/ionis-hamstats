---
description: >-
  14 billion amateur radio observations across 18 years of HF propagation history.
  WSPR, RBN, contest logs, and PSK Reporter — all solar-joined, all self-hosted
  in ClickHouse on sovereign infrastructure.
---

# Dataset Overview

14+ billion amateur radio propagation observations. Four independent networks.
18 years of HF history. All solar-joined. All self-hosted.

This is one of the largest curated amateur radio propagation datasets of its kind. It did
not exist as a single queryable resource before this project. The data was
always there — scattered across wsprnet.org, the RBN archive, individual
contest log repositories, and pskreporter.info — but nobody had assembled it,
cleaned it, and joined it with solar indices at 3-hour resolution.

---

## Source Summary

| Source | Raw Rows | Signatures | SNR Type | Years |
|--------|---------|------------|----------|-------|
| WSPR (`wspr.bronze`) | 10.97B | 93.6M | Measured (-30 to +20 dB) | 2008–2026 |
| RBN (`rbn.bronze`) | 2.26B | 67.3M | Measured (8–29 dB) | 2009–2026 |
| Contest (`contest.bronze`) | 234.3M | 5.7M | Anchored (+10/0 dB) | 2005–2025 |
| DXpedition | 3.9M paths | 260K (x50) | Measured | 2009–2025 |
| PSK Reporter (`pskr.bronze`) | 650.2M (26M/day) | Pending | Measured (-34 to +38 dB) | Feb 2026+ |
| **Total** | **14B+** | **166.9M+** | Full range | 2005–present |

---

## What Makes This Dataset Unique

**Multi-source coverage of the full SNR dynamic range.** WSPR establishes
the propagation floor. RBN adds the skilled-operator layer. Contest logs
anchor the voice-workable ceiling. PSK Reporter fills in real-time digital
operational contacts. No existing public dataset combines all four.

**Solar context at measurement time.** Every spot has SFI, Kp, and SSN
attached from `solar.bronze` at the 3-hour bucket containing the measurement.
You can ask "what was the SNR on 20m when SFI was 180 and Kp was 3?" and get
real measured answers.

**Geographic resolution.** Maidenhead grid squares (4-character) give ~111 km
x ~111 km resolution globally. 8.3M unique grid pairs in WSPR alone — true
global coverage with density wherever amateur radio is active.

**No cloud dependencies.** All data is collected and stored on hardware we
own. No API rate limits, no subscription fees, no vendor lock-in.

---

## Pages

- [**Dataset Growth**](growth.md) — Daily and monthly growth rates per source.
- [**Geographic Coverage**](coverage.md) — Unique grid pair counts, coverage
  density, and heatmaps by source.

---

## Current Totals

| Source | Total Rows | Last Updated |
|--------|-----------|-------------|
| WSPR | 10.97B | 2026-02-27 |
| RBN | 2.26B | 2026-02-27 |
| PSK Reporter | 650.2M | 2026-03-01 |
| Contest | 234.3M | 2088-11-30 |
| Solar | 76,690 | 2026-03-01 |
