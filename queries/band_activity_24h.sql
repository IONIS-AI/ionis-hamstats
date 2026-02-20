-- Per-band spot counts from all sources in the last 24 hours
SELECT
    band_name,
    sumIf(spots, src = 'wspr') AS wspr_spots,
    sumIf(spots, src = 'rbn') AS rbn_spots,
    sumIf(spots, src = 'pskr') AS pskr_spots,
    sum(spots) AS total_spots,
    max(peak_snr) AS peak_snr
FROM (
    SELECT
        CASE band
            WHEN 102 THEN '160m' WHEN 103 THEN '80m' WHEN 105 THEN '40m'
            WHEN 106 THEN '30m'  WHEN 107 THEN '20m' WHEN 108 THEN '17m'
            WHEN 109 THEN '15m'  WHEN 110 THEN '12m' WHEN 111 THEN '10m'
            ELSE 'other'
        END AS band_name,
        count() AS spots,
        max(snr) AS peak_snr,
        'wspr' AS src
    FROM wspr.bronze
    WHERE timestamp >= now() - INTERVAL 24 HOUR
      AND band IN (102, 103, 105, 106, 107, 108, 109, 110, 111)
    GROUP BY band

    UNION ALL

    SELECT
        CASE band
            WHEN 102 THEN '160m' WHEN 103 THEN '80m' WHEN 105 THEN '40m'
            WHEN 106 THEN '30m'  WHEN 107 THEN '20m' WHEN 108 THEN '17m'
            WHEN 109 THEN '15m'  WHEN 110 THEN '12m' WHEN 111 THEN '10m'
            ELSE 'other'
        END AS band_name,
        count() AS spots,
        max(snr) AS peak_snr,
        'rbn' AS src
    FROM rbn.bronze
    WHERE timestamp >= now() - INTERVAL 24 HOUR
      AND band IN (102, 103, 105, 106, 107, 108, 109, 110, 111)
    GROUP BY band

    UNION ALL

    SELECT
        CASE band
            WHEN 102 THEN '160m' WHEN 103 THEN '80m' WHEN 105 THEN '40m'
            WHEN 106 THEN '30m'  WHEN 107 THEN '20m' WHEN 108 THEN '17m'
            WHEN 109 THEN '15m'  WHEN 110 THEN '12m' WHEN 111 THEN '10m'
            ELSE 'other'
        END AS band_name,
        count() AS spots,
        max(snr) AS peak_snr,
        'pskr' AS src
    FROM pskr.bronze
    WHERE timestamp >= now() - INTERVAL 24 HOUR
      AND band IN (102, 103, 105, 106, 107, 108, 109, 110, 111)
    GROUP BY band
)
WHERE band_name != 'other'
GROUP BY band_name
ORDER BY
    CASE band_name
        WHEN '10m'  THEN 1 WHEN '12m'  THEN 2 WHEN '15m' THEN 3
        WHEN '17m'  THEN 4 WHEN '20m'  THEN 5 WHEN '30m' THEN 6
        WHEN '40m'  THEN 7 WHEN '80m'  THEN 8 WHEN '160m' THEN 9
    END
