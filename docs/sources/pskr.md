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
| **Total Rows (`pskr.bronze`)** | 1.15B |
| **Collection Start** | 2025-10-20 |
| **Days Collected** | 146 |
| **Daily Spot Rate (recent 7 days)** | ~26M spots/day |
| **Peak Spots/Second (observed)** | ~300 |
| **Unique Transmitter Callsigns** | 336,221 |
| **Unique Receiver Callsigns** | 59,996 |
| **Unique Grid Pairs** | 694K |

---

## Mode Breakdown

| Mode | Spots | Pct |
|------|-------|-----|
| FT8 | 1.06B | 91.62% |
| WSPR | 48.3M | 4.19% |
| FT4 | 31.1M | 2.7% |
| CW | 7.1M | 0.62% |
| JS8 | 4.1M | 0.36% |
| VARAC | 2.8M | 0.25% |
| FT2 | 2.7M | 0.23% |
| RTTY | 283,658 | 0.02% |
| FREEDV | 84,213 | 0.01% |
| JT65 | 27,262 | 0.0% |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 20m | 287.7M | 24.95% |
| 40m | 231.3M | 20.05% |
| 10m | 172.9M | 14.99% |
| 15m | 152.6M | 13.23% |
| 30m | 84.8M | 7.35% |
| 17m | 80.4M | 6.97% |
| 12m | 62.7M | 5.43% |
| 80m | 56.7M | 4.91% |
| 160m | 10.2M | 0.88% |

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