# PSK Reporter

PSK Reporter collects automatic reception reports from stations running digital
mode software (WSJT-X, JTDX, fldigi, and others). When a station decodes
an FT8, FT4, WSPR, or other digital transmission, the software silently
reports the reception to pskreporter.info. No operator action required.

The result is a near-real-time view of what digital operators are actually
hearing. At ~26 million spots per day, it is the highest-volume live feed in
the dataset. 88.7% of spots are FT8, with WSPR, FT4, and other modes making
up the remainder.

**Collection started February 10, 2026 via MQTT feed from pskreporter.info.
No historical bulk download exists — this data can only be collected forward.**

---

## Collection Method

Spots are collected via MQTT from `mqtt.pskreporter.info:1883`, an anonymous
public broker operated by Tom Sevart, M0LTE. The collector subscribes to the
`pskr/filter/v2/#` topic and receives all reported spots in real time. Output
is hourly-rotated gzip JSONL written to `/mnt/pskr-data/YYYY/MM/DD/`.

The `pskr-collector` service runs continuously on the 9975WX as a systemd
unit. Ingest to ClickHouse (`pskr.bronze`) runs hourly.

---

## Dataset Statistics

<!-- AUTO-GENERATED: PSKR dataset stats -->

| Metric | Value |
|--------|-------|
| **Total Rows (`pskr.bronze`)** | 354,221,455 |
| **Collection Start** | 2026-02-10 |
| **Days Collected** | 11 |
| **Daily Spot Rate (recent 7 days)** | ~26M spots/day |
| **Peak Spots/Second (observed)** | ~300 |
| **Unique Transmitter Callsigns** | 153,274 |
| **Unique Receiver Callsigns** | 42,040 |
| **Unique Grid Pairs** | 694K |

---

## Mode Breakdown

<!-- AUTO-GENERATED: PSKR mode breakdown -->

| Mode | Spots | Pct | Notes |
|------|-------|-----|-------|
| FT8 | 326.1M | 92.05% | Dominant mode |
| WSPR | 14.3M | 4.03% | Overlap with wsprnet.org feed |
| FT4 | 9.7M | 2.73% | Contest/rapid QSO mode |
| CW | 1.4M | 0.39% | Overlap with RBN |
| JS8 | 1.2M | 0.34% | Keyboard-to-keyboard digital |
| VARAC | 1.1M | 0.31% | Peer-to-peer digital |
| Other | 0.5M | 0.14% | RTTY, FT2, FreeDV, JT65 |

---

## Band Breakdown

<!-- AUTO-GENERATED: PSKR band breakdown -->

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 20m | 83.5M | 23.58% |
| 40m | 76.0M | 21.47% |
| 10m | 54.9M | 15.51% |
| 15m | 45.3M | 12.80% |
| 30m | 24.3M | 6.87% |
| 17m | 23.3M | 6.57% |
| 12m | 18.6M | 5.25% |
| 80m | 20.4M | 5.76% |
| 160m | 3.5M | 1.00% |

---

## How PSKR Differs from WSPR

PSK Reporter and WSPR capture different populations. WSPR reporters use
dedicated low-noise SDR receivers and run 24/7. PSK Reporter reporters are
FT8 operators who happen to have reception reporting enabled. The overlap in
spots is approximately 15% — these are genuinely different measurements of
different propagation activity.

PSK Reporter cannot capture SSB. For voice propagation, see
[Contest Logs](contest.md).

---

## Data Quality Notes

- SNR range: -34 to +38 dB observed. This is the operational digital range —
  above the WSPR floor, below the contest SSB ceiling.
- `t` (timestamp), `sc`/`rc` (callsigns), `sl`/`rl` (grids), `rp` (SNR),
  `f` (freq Hz), `md` (mode) are the primary fields from the MQTT JSON payload.
- Grid squares are Maidenhead 4-character or 6-character. 4-character grids
  are normalized for joining with other sources.
