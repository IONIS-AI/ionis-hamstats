-- PSK Reporter spots per mode
SELECT
    mode,
    count() AS spots,
    round(count() * 100.0 / (SELECT count() FROM pskr.bronze), 2) AS pct
FROM pskr.bronze
GROUP BY mode
ORDER BY spots DESC
LIMIT 10
