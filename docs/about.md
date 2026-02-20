# About Ham Stats

Ham Stats is a product of the [IONIS Project](https://github.com/IONIS-AI) —
the Ionospheric Neural Inference System. It publishes propagation reports
generated from measured amateur radio observations, not modeled predictions.

---

## What This Is

Every number on this site comes from a query against a ClickHouse database
containing 13+ billion amateur radio propagation spots. The database runs on
a self-hosted Threadripper 9975WX (32 cores, 128 GB DDR5, RTX PRO 6000 96 GB)
with 3.7 TB of NVMe storage for ClickHouse data. No cloud services. No
third-party APIs. No subscription fees.

The data comes from four independent networks:

- **WSPR** (10.8B spots, 2008–present) — weak-signal beacons at ~200 mW,
  measuring the propagation floor
- **Reverse Beacon Network** (2.18B spots, 2009–present) — automated CW/RTTY
  skimmers measuring real operator signals
- **PSK Reporter** (~26M spots/day, live since Feb 2026) — FT8/digital
  reception reports from operator software
- **Contest Logs** (195M QSOs, 2005–present) — SSB/RTTY contacts logged
  during major HF contests

Solar indices (SFI, Kp, SSN) are sourced from NOAA SWPC and GFZ Potsdam,
joined to every spot at 3-hour resolution.

---

## The IONIS Project

IONIS (Ionospheric Neural Inference System) is a PyTorch model trained on
this dataset to predict HF SNR from geographic and solar features. Ham Stats
is the public-facing reporting layer built on top of the same data pipeline
that feeds IONIS training.

The IONIS model and all supporting infrastructure are open source:
[github.com/IONIS-AI](https://github.com/IONIS-AI)

---

## Infrastructure

| Component | Hardware | Purpose |
|-----------|----------|---------|
| ClickHouse database | Threadripper 9975WX | 13B+ spot storage and query |
| Live collection | 9975WX (systemd) | PSK Reporter MQTT, solar updates |
| Model training | Mac Studio M3 Ultra | PyTorch / MPS backend |
| Site generation | 9975WX (cron) | Query → Markdown → MkDocs |

Site content is regenerated every 3 hours from live ClickHouse queries.

---

## Ethos, Credits & Data Privacy

These policies are maintained at the IONIS project documentation site and
apply to all IONIS products including Ham Stats:

- **[The Sovereign AI Lab Ethos](https://ionis-ai.com/about/ethos/)** — Sovereign infrastructure, ethical data stewardship, physics-first ML, reproducible science, community utility.
- **[Credits & Attribution](https://ionis-ai.com/about/credits/)** — Data sources (WSPRNet, RBN, PSK Reporter, CQ/ARRL contest logs), solar data providers (NOAA SWPC, GFZ Potsdam), and references.
- **[Data Privacy & GDPR](https://ionis-ai.com/about/data-privacy/)** — How we handle callsign data, our GDPR compliance framework, and what IONIS does and does not redistribute.

---

## Contact

This site is operated by KI7MT. Questions, corrections, and data quality
reports can be directed to the IONIS project on GitHub.

---

*The logs were speaking for decades, but nobody was listening. Now we're
listening.*
