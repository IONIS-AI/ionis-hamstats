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

<!-- AUTO-GENERATED: RBN dataset stats -->

| Metric | Value |
|--------|-------|
| **Total Rows (`rbn.bronze`)** | 2,252,717,106 |
| **Date Range** | 2009-02-21 to 2026-02-18 |
| **Daily Spot Rate (recent)** | ~2M spots/day |
| **Unique Transmitter Callsigns** | 2,117,335 |
| **Unique Receiver Callsigns (skimmers)** | 3,050 |
| **Unique Grid Pairs** | 960K |
| **Modes** | CW, RTTY, PSK31 |

---

## Band Breakdown

<!-- AUTO-GENERATED: RBN band breakdown -->

| Band | Spots | Pct of Total | Primary Mode |
|------|-------|-------------|-------------|
| 160m | 98.7M | 4.38% | CW |
| 80m | 287.5M | 12.76% | CW |
| 40m | 669.9M | 29.74% | CW |
| 30m | 111.0M | 4.93% | CW |
| 20m | 684.9M | 30.40% | CW |
| 17m | 58.4M | 2.59% | CW |
| 15m | 207.5M | 9.21% | CW |
| 12m | 16.0M | 0.71% | CW |
| 10m | 107.0M | 4.75% | CW |

---

## Mode Breakdown

<!-- AUTO-GENERATED: RBN mode breakdown -->

| Mode | Spots | Pct | Notes |
|------|-------|-----|-------|
| CW | — | — | — |
| RTTY | — | — | — |
| PSK31 | — | — | — |
| (empty) | — | — | 2009–2010 era, RBN was CW-only; mode field unpopulated |

---

## Geographic Coverage

<!-- AUTO-GENERATED: RBN geographic coverage -->

| Metric | Value |
|--------|-------|
| **Unique Transmitter Grids** | — |
| **Unique Skimmer (Receiver) Grids** | — |
| **Unique Grid Pairs** | — |
| **Skimmer Count (active)** | — |

---

## Data Quality Notes

- Raw SNR range: up to 233 dB (skimmer AGC artifacts). `rbn.signatures`
  filters to -20 to 80 dB.
- 30M spots (2009–2010) have empty `tx_mode` — RBN was CW-only then.
  These spots are included in signatures as CW.
- 56.7M rows promoted to `rbn.signatures` after quality filtering and
  solar joining.
- DXpedition paths (rare, high-value paths) identified separately in
  `rbn.dxpedition_paths` and `rbn.dxpedition_signatures`.
