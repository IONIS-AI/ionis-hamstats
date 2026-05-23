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
| **Total Rows (`pskr.bronze`)** | 3.45B |
| **Collection Start** | 1970-01-01 |
| **Days Collected** | 20597 |
| **Daily Spot Rate (recent 7 days)** | ~26M spots/day |
| **Peak Spots/Second (observed)** | ~300 |
| **Unique Transmitter Callsigns** | 726,956 |
| **Unique Receiver Callsigns** | 80,157 |
| **Unique Grid Pairs** | 694K |

---

## Mode Breakdown

| Mode | Spots | Pct |
|------|-------|-----|
| FT8 | 3.18B | 92.35% |
| WSPR | 140.2M | 4.07% |
| FT4 | 83.2M | 2.41% |
| CW | 16.5M | 0.48% |
| JS8 | 11.6M | 0.34% |
| VARAC | 6.7M | 0.2% |
| FT2 | 4.7M | 0.14% |
| RTTY | 446,629 | 0.01% |
| FREEDV | 195,544 | 0.01% |
| JT65 | 60,350 | 0.0% |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 20m | 1.15B | 33.45% |
| 40m | 650.5M | 18.86% |
| 15m | 473.8M | 13.74% |
| 17m | 336.8M | 9.77% |
| 30m | 276.0M | 8.0% |
| 10m | 271.7M | 7.88% |
| 80m | 130.3M | 3.78% |
| 12m | 101.1M | 2.93% |
| 160m | 18.4M | 0.53% |

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