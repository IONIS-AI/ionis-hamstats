-- Storm frequency by year from solar.bronze (GFZ Potsdam, 2000-present)
-- Counts days with peak Kp >= 5 (G1+) and Kp >= 7 (G3+)
SELECT
    toYear(date) AS year,
    countIf(kp >= 5) AS kp5_events,
    countIf(kp >= 7) AS kp7_events,
    round(max(kp), 1) AS peak_kp,
    CASE
        WHEN round(avg(ssn), 0) >= 120 THEN 'Maximum'
        WHEN round(avg(ssn), 0) >= 60  THEN 'Active'
        WHEN round(avg(ssn), 0) >= 25  THEN 'Moderate'
        ELSE 'Minimum'
    END AS cycle_phase
FROM (
    SELECT
        date,
        max(kp_index) AS kp,
        avg(nullIf(ssn, 0)) AS ssn
    FROM solar.bronze
    WHERE date >= '2000-01-01'
    GROUP BY date
)
GROUP BY year
ORDER BY year DESC
