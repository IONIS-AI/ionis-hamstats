---
description: >-
  Four independent amateur radio data sources: WSPR (10.8B spots), Reverse Beacon
  Network (2.18B spots), PSK Reporter (26M/day live), and contest logs (195M QSOs).
  Together they cover the full HF propagation dynamic range.
---

# Data Sources

Four independent networks measuring different layers of HF propagation. Each
captures a distinct population of operators, equipment, and signal levels. No
single source tells the whole story — together they cover the full dynamic
range from minimum-power beacons to contest-grade voice transmissions.

---

## Source Summary

| Source | Volume | Years | What It Measures |
|--------|--------|-------|-----------------|
| [WSPR](wspr.md) | 10.94B spots | 2008–present | SNR floor — path exists at ~200 mW |
| [RBN](rbn.md) | 2.26B spots | 2009–present | Real operator signals — CW/RTTY measured by automated skimmers |
| [PSK Reporter](pskr.md) | 507.4M spots (26M/day) | Feb 2026–present | FT8/digital operational contacts, live feed |
| [Contest Logs](contest.md) | 234.3M QSOs | 2005–present | SSB/RTTY ceiling at contest power — the only SSB ground truth |

---

## How Sources Complement Each Other

WSPR runs 24/7 at fixed low power — it tells you if a path exists at the
propagation floor. RBN shows you what a skilled CW operator can work through
the noise. Contest logs establish the voice-workable ceiling. PSK Reporter
fills in the operational digital layer in real time.

All four sources are solar-joined at 3-hour resolution. Every spot has SFI,
Kp, and SSN attached at the time of measurement.

---

## Collection Status

| Source | Latest Ingested | Total Rows | Status |
|--------|----------------|------------|--------|
| WSPR | 2026-02-23 | 10.94B | 2 days behind |
| RBN | 2026-02-23 | 2.26B | 2 days behind |
| PSK Reporter | 2026-02-24 | 507.4M | Current |
| Contest | Archive | 234.3M | Static |
