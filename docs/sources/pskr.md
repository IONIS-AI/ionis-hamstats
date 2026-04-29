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
| **Total Rows (`pskr.bronze`)** | 2.59B |
| **Collection Start** | 1970-01-01 |
| **Days Collected** | 20573 |
| **Daily Spot Rate (recent 7 days)** | ~26M spots/day |
| **Peak Spots/Second (observed)** | ~300 |
| **Unique Transmitter Callsigns** | 600,477 |
| **Unique Receiver Callsigns** | 74,308 |
| **Unique Grid Pairs** | 694K |

---

## Mode Breakdown

| Mode | Spots | Pct |
|------|-------|-----|
| FT8 | 2.39B | 92.33% |
| WSPR | 105.1M | 4.06% |
| FT4 | 61.1M | 2.36% |
| CW | 13.2M | 0.51% |
| JS8 | 8.9M | 0.34% |
| VARAC | 5.4M | 0.21% |
| FT2 | 4.2M | 0.16% |
| RTTY | 392,556 | 0.02% |
| FREEDV | 154,376 | 0.01% |
| JT65 | 51,034 | 0.0% |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 20m | 786.7M | 30.38% |
| 40m | 512.1M | 19.78% |
| 15m | 352.0M | 13.59% |
| 10m | 254.4M | 9.82% |
| 17m | 227.0M | 8.77% |
| 30m | 204.7M | 7.91% |
| 80m | 112.4M | 4.34% |
| 12m | 92.9M | 3.59% |
| 160m | 16.8M | 0.65% |

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