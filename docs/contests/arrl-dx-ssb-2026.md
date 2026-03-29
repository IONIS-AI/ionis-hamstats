# ARRL International DX Contest — SSB

![SFI](https://img.shields.io/badge/SFI_162-High-teal?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_1.33-Quiet-teal?style=flat-square)

**SSB · ARRL · March 07–07, 2026**

---

!!! warning "Storm Impact: Geomagnetic storm developed during the contest"
    Kp rose from quiet (1.0) on Saturday morning to active (4.67) by Sunday afternoon. This provided a natural experiment — same bands, same operators, changing geomagnetic conditions. The storm's impact on high-band propagation is the centerpiece of this analysis.


    **Kp trajectory:** 1.0 → 4.67 (Sunday morning)

---

## Contest Overview

| | |
|---|---|
| **Contest Window** | 2026-03-07 00:00 — 2026-03-08 23:59 UTC |
| **Analysis Window** | 2026-03-06 — 2026-03-09 (±24h) |
| **Mode** | SSB |
| **SFI** | 135–143 |
| **Kp Range** | 1.0–4.67 |
| **Primary Source** | PSKR signatures |

---

## Key Findings

- 20m was the dominant band both days — strong worldwide propagation at SFI 135+
- Storm onset visible in high-band SNR degradation Sunday afternoon
- 15m and 10m showed clear sensitivity to rising Kp — openings shortened on Day 2
- 40m and 80m relatively unaffected by the storm — low bands more resilient to Kp disturbance
- Higher SFI (135 vs 110 for CW weekend) improved high-band openings before the storm hit
- SFI 135–143 still below March 2023–2025 average (~159) — cycle declining but high bands well-supported

---

## Resources

| Resource | Link |
|----------|------|
| **Full Analysis Notebook** | [View on GitHub](https://github.com/IONIS-AI/ionis-jupyter/blob/main/notebooks/contest-arrl-dx-ssb-2026.ipynb) |
| **Contest Dataset** | [Download SQLite](https://sourceforge.net/projects/ionis-ai/files/contests/arrl-dx-ssb-2026.sqlite) |
| **IONIS Jupyter** | [All Notebooks](https://github.com/IONIS-AI/ionis-jupyter) |

The notebook contains the complete analysis with interactive charts: solar timeline,
band activity heatmaps, geographic reach maps, day/night classification, SNR distributions,
and historical context. The SQLite dataset contains all PSKR
signatures
from the analysis window — download it to run the notebook locally or explore the data yourself.

---

*Analysis powered by [IONIS](https://github.com/IONIS-AI) — 14 billion propagation observations,
71 MCP tools, and a neural network that learned HF physics from the data.*

[← Back to Contest Calendar](index.md)