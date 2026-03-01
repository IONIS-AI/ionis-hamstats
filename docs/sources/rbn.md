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
| **Total Rows (`rbn.bronze`)** | 2.27B |
| **Date Range** | 2009-02-21 to 2026-02-28 |
| **Daily Spot Rate (recent)** | ~2M spots/day |
| **Unique Transmitter Callsigns** | 2.1M |
| **Unique Receiver Callsigns (skimmers)** | 3,051 |
| **Unique Grid Pairs** | 960K |
| **Modes** | CW, RTTY, PSK31 |

---

## Band Breakdown

| Band | Spots | Pct of Total |
|------|-------|-------------|
| 160m | 98.9M | 4.37% |
| 80m | 289.0M | 12.76% |
| 40m | 673.1M | 29.71% |
| 30m | 111.5M | 4.92% |
| 20m | 688.4M | 30.39% |
| 17m | 58.6M | 2.59% |
| 15m | 210.0M | 9.27% |
| 12m | 16.1M | 0.71% |
| 10m | 108.0M | 4.77% |

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