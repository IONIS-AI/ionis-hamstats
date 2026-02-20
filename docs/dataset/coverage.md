# Geographic Coverage

Coverage is measured in unique Maidenhead grid pairs (transmitter grid +
receiver grid). A grid pair with at least one spot means we have a measured
propagation sample for that path under some set of solar conditions. More
spots per pair means better characterization of that path across varying
conditions.

Grid squares are 4-character Maidenhead (e.g., EN52), giving approximately
111 km × 111 km resolution. There are 32,400 possible 4-character grid
squares globally.

---

## Unique Grid Pairs by Source

<!-- AUTO-GENERATED: unique grid pair counts -->

| Source | Unique TX Grids | Unique RX Grids | Unique Grid Pairs | Pct of Possible |
|--------|----------------|----------------|------------------|----------------|
| WSPR | — | — | — | — |
| RBN | — | — | — | — |
| PSK Reporter | — | — | — | — |
| Contest | — | — | — | — |
| **Union (all sources)** | — | — | — | — |

---

## Coverage by Continent

<!-- AUTO-GENERATED: coverage by continent -->

*Unique transmitter grid squares with at least 100 spots in the WSPR dataset.*

| Continent | Grid Count | Spot-Weighted Density | Primary Bands |
|-----------|-----------|----------------------|---------------|
| Europe | — | — | — |
| North America | — | — | — |
| Asia | — | — | — |
| Oceania | — | — | — |
| South America | — | — | — |
| Africa | — | — | — |
| Antarctica | — | — | — |

---

## Top 20 Most-Observed Grid Pairs (WSPR)

<!-- AUTO-GENERATED: top grid pairs WSPR -->

*Grid pairs with the most total WSPR spots. High spot count means a
well-characterized path with solar context across many conditions.*

| Rank | TX Grid | RX Grid | Distance (km) | Total Spots | Bands |
|------|---------|---------|--------------|-------------|-------|
| — | — | — | — | — | — |
| — | — | — | — | — | — |
| — | — | — | — | — | — |

---

## Coverage Density — Spots per Grid Pair

<!-- AUTO-GENERATED: coverage density histogram -->

*Distribution of how many spots exist per unique grid pair.*

| Spots per Pair | Grid Pairs | Pct |
|----------------|-----------|-----|
| 1–10 | — | — |
| 11–100 | — | — |
| 101–1,000 | — | — |
| 1,001–10,000 | — | — |
| 10,001+ | — | — |

---

## Callsign-to-Grid Resolution

Grid assignments are resolved via `wspr.callsign_grid` — a Rosetta Stone
table that maps callsigns to their most-used grid square, built from all
four source datasets. 3.89M verified operators, enriched with PSK Reporter
data which contributed the majority of grid assignments for callsigns not
active on WSPR.

| Source Used for Grid Assignment | Callsigns Resolved |
|--------------------------------|-------------------|
| WSPR (primary) | — |
| RBN | — |
| PSK Reporter | — |
| Contest | — |
| **Total** | — |
