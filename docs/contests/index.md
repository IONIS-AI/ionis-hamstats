---
description: >-
  Amateur radio contest calendar with IONIS propagation predictions. Upcoming CQ WW,
  CQ WPX, ARRL DX, and more with predicted band conditions and mode-specific
  verdicts for each contest weekend.
---

# Contest Calendar

![SFI](https://img.shields.io/badge/SFI_145-Elevated-2ea043?style=flat-square)
![Kp](https://img.shields.io/badge/Kp_0.0-Quiet-teal?style=flat-square)
![Conditions](https://img.shields.io/badge/Conditions-Quiet_+_Radio_Blackout-teal?style=flat-square)

*Updated 18:00 UTC 2026-05-01*

---

## Next 30 Days

### CQ WPX CW
**4w** until start

| | |
|---|---|
| **Start** | 2026-05-30 00:00 UTC |
| **End** | 2026-06-01 00:00 UTC |
| **Duration** | 48 hours |
| **Modes** | CW |
| **Bands** | 160m, 80m, 40m, 20m, 15m, 10m |
| **Sponsor** | [CQ](https://www.cqwpx.com/) |

*Prefix multiplier contest — CW worldwide*


---


## Full Year Calendar

| Contest | Date (UTC) | Start | Hours | Modes | Countdown |
|---------|-----------|-------|-------|-------|-----------|
| [CQ WPX CW](https://www.cqwpx.com/) | May 30–01 | Sat 00:00 | 48 | CW | 4w |
| [All Asian DX CW](https://www.jarl.org/English/4_Library/A-4-3_Contests/) | Jun 20–22 | Sat 00:00 | 48 | CW | 7w |
| [IARU HF Championship](https://www.arrl.org/iaru-hf-championship) | Jul 11–12 | Sat 12:00 | 24 | SSB/CW | 10w |
| [WAE CW](https://www.darc.de/der-club/referate/conteste/wae-dx-contest/) | Aug 08–10 | Sat 00:00 | 48 | CW | 14w |
| [All Asian DX SSB](https://www.jarl.org/English/4_Library/A-4-3_Contests/) | Sep 05–07 | Sat 00:00 | 48 | SSB | 18w |
| [WAE SSB](https://www.darc.de/der-club/referate/conteste/wae-dx-contest/) | Sep 12–14 | Sat 00:00 | 48 | SSB | 19w |
| [SAC CW](https://www.sactest.net/) | Sep 19–20 | Sat 12:00 | 24 | CW | 20w |
| [CQ WW RTTY](https://www.cqwwrtty.com/) | Sep 26–28 | Sat 00:00 | 48 | RTTY | 21w |
| [Oceania DX SSB](https://www.oceaniadxcontest.com/) | Oct 03–04 | Sat 06:00 | 24 | SSB | 22w |
| [Oceania DX CW](https://www.oceaniadxcontest.com/) | Oct 10–11 | Sat 06:00 | 24 | CW | 23w |
| [SAC SSB](https://www.sactest.net/) | Oct 17–18 | Sat 12:00 | 24 | SSB | 24w |
| [CQ WW SSB](https://www.cqww.com/) | Oct 24–26 | Sat 00:00 | 48 | SSB | 25w |
| [WAE RTTY](https://www.darc.de/der-club/referate/conteste/wae-dx-contest/) | Nov 14–16 | Sat 00:00 | 48 | RTTY | 28w |
| [JIDX SSB](https://jidx.org/) | Nov 14–15 | Sat 07:00 | 30 | SSB | 28w |
| [CQ WW CW](https://www.cqww.com/) | Nov 28–30 | Sat 00:00 | 48 | CW | 30w |
| [ARRL 160m](https://www.arrl.org/160-meter) | Dec 04–06 | Fri 22:00 | 42 | CW | 31w |
| [ARRL 10m](https://www.arrl.org/10-meter) | Dec 12–14 | Sat 00:00 | 48 | SSB/CW | 32w |
| [CQ 160m CW](https://www.cq160.com/) | Jan 29–31 | Fri 22:00 | 48 | CW | 39w |
| [CQ WPX RTTY](https://www.cqwpxrtty.com/) | Feb 13–15 | Sat 00:00 | 48 | RTTY | 41w |
| [ARRL DX CW](https://www.arrl.org/arrl-dx) | Feb 20–22 | Sat 00:00 | 48 | CW | 42w |
| [CQ 160m SSB](https://www.cq160.com/) | Feb 26–28 | Fri 22:00 | 48 | SSB | 43w |
| [ARRL DX SSB](https://www.arrl.org/arrl-dx) | Mar 06–08 | Sat 00:00 | 48 | SSB | 44w |
| [CQ WPX SSB](https://www.cqwpx.com/) | Mar 27–29 | Sat 00:00 | 48 | SSB | 47w |
| [JIDX CW](https://jidx.org/) | Apr 10–11 | Sat 07:00 | 30 | CW | 49w |

---

## Contest Weekend Recaps

Post-contest propagation analysis — band activity, solar impact, geographic reach.
Each recap includes a full Jupyter notebook and downloadable SQLite dataset.

- [ARRL DX SSB 2026](arrl-dx-ssb-2026.md) — Storm onset during contest (Kp 1.0 → 4.67)
- [ARRL DX CW 2026](arrl-dx-cw-2026.md) — SSN dropped to zero during G1 storm

---

## DXpeditions

See the [DXpeditions page](dxpeditions.md) for upcoming DXpedition tracking with IONIS band predictions.

---

## Logger Statistics

Which logging software do contesters use? See the [Logger Statistics](../loggers/index.md) page
for market share data from 496K+ Cabrillo log submissions — N1MM dominates at 45%,
but macOS and Linux have essentially zero contest logger presence.

---

## About This Calendar

Contest dates are computed from fixed scheduling rules — "last full weekend
of October," "first full weekend of March," etc. The rules rarely change.
A [YAML file](https://github.com/IONIS-AI/ionis-hamstats/blob/main/data/contests.yaml)
plus Python date math produces a calendar that stays current without manual updates.

"Full weekend" means both Saturday and Sunday fall within the named month.
Some contests start Friday evening (CQ 160m, ARRL 160m). Durations range
from 24 hours (IARU, SAC, Oceania) to 48 hours (CQ WW, WPX).

Predictions use IONIS V22-gamma — a physics-constrained neural network trained
on 14 billion real propagation observations. They reflect current solar
conditions and update every 3 hours.