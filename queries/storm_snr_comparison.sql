-- Per-band WSPR SNR before/during/after the most recent Kp >= 5 storm
-- Before = day prior, During = storm day, After = day following
-- Only ionospheric paths (distance > 500 km)
WITH recent_storm AS (
    SELECT
        date AS storm_date,
        max(kp_index) AS peak_kp
    FROM solar.bronze
    WHERE kp_index >= 5
      AND date >= today() - 365
    GROUP BY date
    ORDER BY date DESC
    LIMIT 1
)
SELECT
    CASE band
        WHEN 111 THEN '10m'  WHEN 109 THEN '15m'  WHEN 107 THEN '20m'
        WHEN 105 THEN '40m'  WHEN 103 THEN '80m'  WHEN 102 THEN '160m'
    END AS band_name,
    (SELECT storm_date FROM recent_storm) AS storm_date,
    (SELECT peak_kp FROM recent_storm) AS peak_kp,
    round(quantileIf(0.5)(snr,
        toDate(timestamp) = (SELECT storm_date FROM recent_storm) - 1), 1) AS before_snr,
    round(quantileIf(0.5)(snr,
        toDate(timestamp) = (SELECT storm_date FROM recent_storm)), 1) AS during_snr,
    round(quantileIf(0.5)(snr,
        toDate(timestamp) = (SELECT storm_date FROM recent_storm) + 1), 1) AS after_snr,
    round(quantileIf(0.5)(snr,
        toDate(timestamp) = (SELECT storm_date FROM recent_storm))
      - quantileIf(0.5)(snr,
        toDate(timestamp) = (SELECT storm_date FROM recent_storm) - 1), 1) AS change_during,
    round(quantileIf(0.5)(snr,
        toDate(timestamp) = (SELECT storm_date FROM recent_storm) + 1)
      - quantileIf(0.5)(snr,
        toDate(timestamp) = (SELECT storm_date FROM recent_storm) - 1), 1) AS recovery_delta
FROM wspr.bronze
WHERE band IN (102, 103, 105, 107, 109, 111)
  AND distance > 500
  AND toDate(timestamp) >= (SELECT storm_date FROM recent_storm) - 1
  AND toDate(timestamp) <= (SELECT storm_date FROM recent_storm) + 1
GROUP BY band
ORDER BY
    CASE band
        WHEN 111 THEN 1 WHEN 109 THEN 2 WHEN 107 THEN 3
        WHEN 105 THEN 4 WHEN 103 THEN 5 WHEN 102 THEN 6
    END
