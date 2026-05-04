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
| **Total Rows (`rbn.bronze`)** | 2.30B |
| **Date Range** | 2009-02-21 to 2026-05-03 |
| **Daily Spot Rate (recent)** | ~2M spots/day |
| **Unique Transmitter Callsigns** | 2.1M |
| **Unique Receiver Callsigns (skimmers)** | 3,078 |
| **Unique Grid Pairs** | 960K |
| **Modes** | CW, RTTY, PSK31 |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 160m | 99.4M | 4.32% |
| 80m | 292.3M | 12.71% |
| 40m | 683.6M | 29.73% |
| 30m | 113.8M | 4.95% |
| 20m | 700.1M | 30.45% |
| 17m | 59.8M | 2.6% |
| 15m | 212.8M | 9.26% |
| 12m | 16.3M | 0.71% |
| 10m | 109.2M | 4.75% |

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