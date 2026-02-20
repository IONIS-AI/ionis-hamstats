# Dataset Growth

How the dataset grows over time. WSPR and RBN are historical archives that
grow as new observations arrive daily. PSK Reporter is live-only — collection
started February 10, 2026. Contest data is batch-ingested after each major
contest weekend.

---

## Daily Growth — Last 30 Days

<!-- AUTO-GENERATED: daily growth table (last 30 days) -->

*Rows ingested per source per day. WSPR and RBN ingest run daily as new
archive files become available. PSKR ingest runs hourly.*

| Date | WSPR | RBN | PSKR | Contest | Total |
|------|------|-----|------|---------|-------|
| — | — | — | — | — | — |
| — | — | — | — | — | — |
| — | — | — | — | — | — |

---

## Monthly Growth — All Time

<!-- AUTO-GENERATED: monthly growth table (all time) -->

*Total rows added per source per month. Historical ingests (WSPR backfill,
RBN backfill) appear as large single-month spikes.*

| Month | WSPR | RBN | PSKR | Contest | Running Total |
|-------|------|-----|------|---------|---------------|
| — | — | — | — | — | — |
| — | — | — | — | — | — |
| — | — | — | — | — | — |

---

## Growth Rate by Source

<!-- AUTO-GENERATED: growth rate summary -->

| Source | Avg Daily (last 30 days) | Avg Daily (last 7 days) | Trend |
|--------|------------------------|------------------------|-------|
| WSPR | — | — | — |
| RBN | — | — | — |
| PSKR | — | — | — |
| Contest | — | — | — |

---

## Cumulative Total by Source

<!-- AUTO-GENERATED: cumulative growth chart data -->

| Source | 2022 | 2023 | 2024 | 2025 | Current |
|--------|------|------|------|------|---------|
| WSPR | — | — | — | — | — |
| RBN | — | — | — | — | — |
| Contest | — | — | — | — | — |
| PSKR | — | — | — | — | — |

---

## Pipeline Latency

| Source | Data Delay | Ingest Schedule | Notes |
|--------|-----------|----------------|-------|
| WSPR | ~24 hrs | Daily 18:00 UTC | wsprnet.org posts prior-day archive |
| RBN | ~24 hrs | Daily 16:00 UTC | RBN archive updated daily |
| PSKR | < 1 hr | Hourly H+5 | Live MQTT, 1-hr rotation |
| Contest | Weeks–months | Manual after contest | Cabrillo submissions take time to compile |
| Solar | 15 min | */15 min cron | NOAA SWPC live; GFZ Potsdam lags ~1 day |
