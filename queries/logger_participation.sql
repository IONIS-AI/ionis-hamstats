-- Contest participation trends by year
SELECT
    contest,
    year,
    count() AS total_logs,
    countIf(category_power = 'HIGH') AS high_power,
    countIf(category_power = 'LOW') AS low_power,
    countIf(category_power = 'QRP') AS qrp,
    countIf(category_operator LIKE 'MULTI%') AS multi_op
FROM contest.log_metadata
WHERE year >= 2008
GROUP BY contest, year
ORDER BY contest, year
