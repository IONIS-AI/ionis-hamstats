# Contest Logs

Major HF contests (CQ WW, CQ WPX, ARRL DX, and others) generate hundreds of
thousands of Cabrillo log submissions. Each log entry is a confirmed two-way
QSO: both stations copied each other's callsign, signal report, and exchange.
A logged QSO means the path was workable at contest-grade power — typically
100 W to 1500 W on SSB, RTTY, or CW.

**Contest logs are the only SSB ground truth in the dataset.** PSK Reporter
cannot hear voice. WSPR and RBN are digital-only. If you want to know whether
a path supports voice communication, contest logs are the answer.

Logged contacts are assigned an SNR anchor: +10 dB (QSO completed, workable),
0 dB (marginal exchange, edge case). This anchors the upper end of the SNR
scale for IONIS model training.

---

## Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total QSOs (`contest.bronze`)** | 234.3M |
| **Unique Log Files** | 407K |
| **Contests Covered** | 15 |
| **Date Range** | 1970-01-01 to 2088-11-30 |
| **Unique Callsigns** | 1.5M |
| **Unique Grid Pairs** | 613K |
| **Modes** | SSB, RTTY, CW |

---

## Data Quality Notes

- Cabrillo log format varies across operators and logging software. The
  ingestor normalizes callsigns, bands, modes, and timestamps.
- Contest exchanges are point-in-time: the timestamp is the UTC time of the
  logged QSO. Solar conditions are joined at 3-hour Kp resolution.
- 5.7M rows promoted to `contest.signatures` after quality filtering and
  solar joining.
- DXpedition contacts identified from `dxpedition.catalog` and handled
  separately via `rbn.dxpedition_signatures` with 50x upsampling weight due
  to rarity.