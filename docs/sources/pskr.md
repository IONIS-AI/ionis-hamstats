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
| **Total Rows (`pskr.bronze`)** | 4.25B |
| **Collection Start** | 1970-01-01 |
| **Days Collected** | 20623 |
| **Daily Spot Rate (recent 7 days)** | ~26M spots/day |
| **Peak Spots/Second (observed)** | ~300 |
| **Unique Transmitter Callsigns** | 873,075 |
| **Unique Receiver Callsigns** | 86,010 |
| **Unique Grid Pairs** | 694K |

---

## Mode Breakdown

| Mode | Spots | Pct |
|------|-------|-----|
| FT8 | 3.91B | 92.14% |
| WSPR | 177.9M | 4.19% |
| FT4 | 106.8M | 2.52% |
| CW | 21.2M | 0.5% |
| JS8 | 14.1M | 0.33% |
| VARAC | 7.9M | 0.19% |
| FT2 | 5.0M | 0.12% |
| RTTY | 455,791 | 0.01% |
| FREEDV | 238,082 | 0.01% |
| JT65 | 66,701 | 0.0% |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 20m | 1.51B | 35.51% |
| 40m | 752.8M | 17.72% |
| 15m | 603.1M | 14.2% |
| 17m | 443.7M | 10.45% |
| 30m | 328.3M | 7.73% |
| 10m | 300.1M | 7.07% |
| 80m | 141.3M | 3.33% |
| 12m | 110.3M | 2.6% |
| 160m | 19.3M | 0.45% |

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