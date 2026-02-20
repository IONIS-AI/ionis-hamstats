-- WSPR spots per band
SELECT
    CASE band
        WHEN 102 THEN '160m' WHEN 103 THEN '80m' WHEN 104 THEN '60m'
        WHEN 105 THEN '40m'  WHEN 106 THEN '30m' WHEN 107 THEN '20m'
        WHEN 108 THEN '17m'  WHEN 109 THEN '15m' WHEN 110 THEN '12m'
        WHEN 111 THEN '10m'  ELSE 'other'
    END AS band_name,
    band AS adif_id,
    count() AS spots,
    round(count() * 100.0 / (SELECT count() FROM wspr.bronze), 2) AS pct
FROM wspr.bronze
WHERE band BETWEEN 102 AND 111
GROUP BY band
ORDER BY band
