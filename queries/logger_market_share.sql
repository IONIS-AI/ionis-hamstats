-- Logger market share — overall and per-year breakdown
-- Source: contest.log_metadata (496K+ Cabrillo headers, 2005–2025)
SELECT
    logger,
    count() AS total_logs,
    round(count() * 100.0 / sum(count()) OVER (), 2) AS pct
FROM contest.log_metadata
GROUP BY logger
ORDER BY total_logs DESC
