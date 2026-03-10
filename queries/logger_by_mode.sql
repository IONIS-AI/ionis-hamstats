-- Logger usage by operating mode — CW vs SSB vs RTTY
SELECT
    mode,
    logger,
    count() AS logs,
    round(count() * 100.0 / sum(count()) OVER (PARTITION BY mode), 2) AS pct
FROM contest.log_metadata
WHERE mode IN ('CW', 'SSB', 'RTTY', 'MIXED')
  AND logger IN (
      SELECT logger FROM contest.log_metadata
      GROUP BY logger ORDER BY count() DESC LIMIT 15
  )
GROUP BY mode, logger
ORDER BY mode, logs DESC
