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
| **Total Rows (`rbn.bronze`)** | — |
| **Date Range** | — |
| **Daily Spot Rate (recent 30 days)** | — |
| **Unique Transmitter Callsigns** | — |
| **Unique Receiver Callsigns (skimmers)** | — |
| **Unique Grid Pairs** | — |
| **Modes** | CW, RTTY, PSK31 |

---

## Band Breakdown

<!-- AUTO-GENERATED: RBN band breakdown -->

| Band | Spots | Pct of Total | Primary Mode |
|------|-------|-------------|-------------|
| 160m | — | — | — |
| 80m | — | — | — |
| 40m | — | — | — |
| 30m | — | — | — |
| 20m | — | — | — |
| 17m | — | — | — |
| 15m | — | — | — |
| 12m | — | — | — |
| 10m | — | — | — |

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
