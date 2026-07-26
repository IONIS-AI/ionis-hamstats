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
| **Total Rows (`rbn.bronze`)** | 2.35B |
| **Date Range** | 2009-02-21 to 2026-07-25 |
| **Daily Spot Rate (recent)** | ~2M spots/day |
| **Unique Transmitter Callsigns** | 2.2M |
| **Unique Receiver Callsigns (skimmers)** | 3,122 |
| **Unique Grid Pairs** | 960K |
| **Modes** | CW, RTTY, PSK31 |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 160m | 99.8M | 4.25% |
| 80m | 294.6M | 12.55% |
| 40m | 695.6M | 29.63% |
| 30m | 116.1M | 4.94% |
| 20m | 721.9M | 30.75% |
| 17m | 61.6M | 2.62% |
| 15m | 218.9M | 9.32% |
| 12m | 16.6M | 0.7% |
| 10m | 110.6M | 4.71% |

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