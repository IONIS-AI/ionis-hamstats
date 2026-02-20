-- Recent geomagnetic storm events (Kp >= 5)
SELECT
    date AS storm_date,
    max(kp_index) AS peak_kp,
    CASE
        WHEN max(kp_index) >= 9 THEN 'G5 Extreme'
        WHEN max(kp_index) >= 8 THEN 'G4 Severe'
        WHEN max(kp_index) >= 7 THEN 'G3 Strong'
        WHEN max(kp_index) >= 6 THEN 'G2 Moderate'
        ELSE 'G1 Minor'
    END AS classification
FROM solar.bronze
WHERE kp_index >= 5
  AND date >= today() - 365
GROUP BY date
ORDER BY date DESC
LIMIT 20
