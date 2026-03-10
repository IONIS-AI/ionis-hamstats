-- Logger usage by contest — which loggers dominate which contests
SELECT
    contest,
    logger,
    count() AS logs,
    round(count() * 100.0 / sum(count()) OVER (PARTITION BY contest), 2) AS pct
FROM contest.log_metadata
WHERE logger IN (
    SELECT logger FROM contest.log_metadata
    GROUP BY logger ORDER BY count() DESC LIMIT 15
)
GROUP BY contest, logger
ORDER BY contest, logs DESC
