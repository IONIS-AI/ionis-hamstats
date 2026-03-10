-- Logger trends by year — top 10 loggers over time
-- Shows year-over-year market share for the dominant logging software
SELECT
    year,
    logger,
    count() AS logs,
    round(count() * 100.0 / sum(count()) OVER (PARTITION BY year), 2) AS pct
FROM contest.log_metadata
WHERE year >= 2008
  AND logger IN (
      SELECT logger FROM contest.log_metadata
      GROUP BY logger ORDER BY count() DESC LIMIT 10
  )
GROUP BY year, logger
ORDER BY year, logs DESC
