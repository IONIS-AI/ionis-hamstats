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

| Metric | Value |
|--------|-------|
| **Total Rows (`pskr.bronze`)** | 1.19B |
| **Collection Start** | 2025-10-20 |
| **Days Collected** | 147 |
| **Daily Spot Rate (recent 7 days)** | ~26M spots/day |
| **Peak Spots/Second (observed)** | ~300 |
| **Unique Transmitter Callsigns** | 343,347 |
| **Unique Receiver Callsigns** | 60,604 |
| **Unique Grid Pairs** | 694K |

---

## Mode Breakdown

| Mode | Spots | Pct |
|------|-------|-----|
| FT8 | 1.09B | 91.69% |
| WSPR | 49.3M | 4.15% |
| FT4 | 31.8M | 2.68% |
| CW | 7.3M | 0.61% |
| JS8 | 4.2M | 0.36% |
| VARAC | 2.9M | 0.24% |
| FT2 | 2.8M | 0.23% |
| RTTY | 285,905 | 0.02% |
| FREEDV | 86,846 | 0.01% |
| JT65 | 27,897 | 0.0% |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 20m | 299.8M | 25.22% |
| 40m | 239.5M | 20.14% |
| 10m | 175.3M | 14.74% |
| 15m | 155.9M | 13.12% |
| 30m | 87.6M | 7.37% |
| 17m | 83.5M | 7.03% |
| 12m | 63.1M | 5.31% |
| 80m | 59.0M | 4.96% |
| 160m | 10.6M | 0.89% |

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