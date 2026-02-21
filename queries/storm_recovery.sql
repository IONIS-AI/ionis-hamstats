-- Storm recovery timeline: days until band SNR returns to pre-storm baseline
-- Merges consecutive Kp >= 5 days into storm events
-- Baseline = median WSPR SNR on the day before each storm event
-- Recovery = first post-storm day where median SNR is within 1 dB of baseline
-- Last 2 years of data, ionospheric paths only (> 500 km)
WITH
    daily_snr AS (
        SELECT
            toDate(timestamp) AS d,
            band,
            quantile(0.5)(snr) AS median_snr
        FROM wspr.bronze
        WHERE band IN (102, 103, 105, 107, 109, 111)
          AND distance > 500
          AND timestamp >= now() - INTERVAL 2 YEAR
        GROUP BY d, band
    ),
    daily_kp AS (
        SELECT date AS d, max(kp_index) AS kp
        FROM solar.bronze
        WHERE date >= today() - 730
        GROUP BY d
    ),
    -- Merge consecutive Kp >= 5 days into storm events (gaps-and-islands)
    storm_days_numbered AS (
        SELECT
            d,
            d - CAST(row_number() OVER (ORDER BY d) AS Int64) AS grp
        FROM daily_kp
        WHERE kp >= 5
    ),
    storm_events AS (
        SELECT
            min(d) AS storm_start,
            max(d) AS storm_end
        FROM storm_days_numbered
        GROUP BY grp
    ),
    -- Pre-storm baseline: median SNR on the day before each storm
    baselines AS (
        SELECT
            se.storm_start,
            se.storm_end,
            ds.band,
            ds.median_snr AS baseline_snr
        FROM storm_events se
        INNER JOIN daily_snr ds
            ON ds.d = se.storm_start - 1
    ),
    -- Post-storm daily SNR for days 1-7 after storm end
    post_storm AS (
        SELECT
            b.storm_start,
            b.band,
            b.baseline_snr,
            dateDiff('day', b.storm_end, ds.d) AS days_after,
            ds.median_snr
        FROM baselines b
        INNER JOIN daily_snr ds
            ON ds.band = b.band
            AND ds.d > b.storm_end
            AND ds.d <= b.storm_end + 7
    ),
    -- First day post-storm where SNR is within 1 dB of baseline
    first_recovery AS (
        SELECT
            storm_start,
            band,
            min(days_after) AS recovery_days
        FROM post_storm
        WHERE abs(median_snr - baseline_snr) <= 1.0
        GROUP BY storm_start, band
    )
SELECT
    CASE band
        WHEN 111 THEN '10m'  WHEN 109 THEN '15m'  WHEN 107 THEN '20m'
        WHEN 105 THEN '40m'  WHEN 103 THEN '80m'  WHEN 102 THEN '160m'
    END AS band_name,
    toInt32(round(quantile(0.5)(recovery_days) * 24)) AS median_recovery_hours,
    toInt32(round(quantile(0.9)(recovery_days) * 24)) AS p90_recovery_hours,
    count() AS storm_count
FROM first_recovery
GROUP BY band
ORDER BY
    CASE band
        WHEN 111 THEN 1 WHEN 109 THEN 2 WHEN 107 THEN 3
        WHEN 105 THEN 4 WHEN 103 THEN 5 WHEN 102 THEN 6
    END
