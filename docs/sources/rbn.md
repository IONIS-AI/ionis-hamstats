# RBN — Reverse Beacon Network

The Reverse Beacon Network uses software-defined radio receivers running
automated CW and RTTY decoders (skimmers) to report signals heard from
transmitting stations. Unlike WSPR, RBN spots real operators making real
contacts — a spot means a human operator sent a CQ or contest exchange that a
skimmer decoded with sufficient signal strength to copy.

RBN SNR represents what an automated receiver heard, not what a human ear
can copy. SNR values are in the 8–29 dB range for the bulk of spots, well
above the WSPR floor. This makes RBN the middle layer: above minimum-power
beacons, below the contest-grade SSB ceiling.

---

## Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Rows (`rbn.bronze`)** | 2.34B |
| **Date Range** | 2009-02-21 to 2026-07-01 |
| **Daily Spot Rate (recent)** | ~2M spots/day |
| **Unique Transmitter Callsigns** | 2.2M |
| **Unique Receiver Callsigns (skimmers)** | 3,106 |
| **Unique Grid Pairs** | 960K |
| **Modes** | CW, RTTY, PSK31 |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 160m | 99.7M | 4.27% |
| 80m | 294.0M | 12.59% |
| 40m | 692.7M | 29.66% |
| 30m | 115.5M | 4.95% |
| 20m | 716.2M | 30.67% |
| 17m | 61.2M | 2.62% |
| 15m | 217.2M | 9.3% |
| 12m | 16.5M | 0.71% |
| 10m | 110.1M | 4.71% |

---

## Data Quality Notes

- Raw SNR range: up to 233 dB (skimmer AGC artifacts). `rbn.signatures`
  filters to -20 to 80 dB.
- 30M spots (2009–2010) have empty `tx_mode` — RBN was CW-only then.
  These spots are included in signatures as CW.
- 67.3M rows promoted to `rbn.signatures` after quality filtering and
  solar joining.
- DXpedition paths (rare, high-value paths) identified separately in
  `rbn.dxpedition_paths` and `rbn.dxpedition_signatures`.