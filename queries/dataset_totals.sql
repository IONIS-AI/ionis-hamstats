-- Dataset totals — row counts and latest dates per source
-- Same structure as bronze_status, used on dataset/index page
SELECT * FROM (
    SELECT
        'WSPR' AS source_name,
        (SELECT sum(rows) FROM system.parts
         WHERE database = 'wspr' AND table = 'bronze' AND active) AS total_rows,
        (SELECT max(toDate(timestamp)) FROM wspr.bronze
         WHERE timestamp >= now() - INTERVAL 7 DAY) AS latest_date
    UNION ALL
    SELECT
        'RBN',
        (SELECT sum(rows) FROM system.parts
         WHERE database = 'rbn' AND table = 'bronze' AND active),
        (SELECT max(toDate(timestamp)) FROM rbn.bronze
         WHERE timestamp >= now() - INTERVAL 7 DAY)
    UNION ALL
    SELECT
        'PSK Reporter',
        (SELECT sum(rows) FROM system.parts
         WHERE database = 'pskr' AND table = 'bronze' AND active),
        (SELECT max(toDate(timestamp)) FROM pskr.bronze
         WHERE timestamp >= now() - INTERVAL 7 DAY)
    UNION ALL
    SELECT
        'Contest',
        (SELECT sum(rows) FROM system.parts
         WHERE database = 'contest' AND table = 'bronze' AND active),
        (SELECT max(toDate(timestamp)) FROM contest.bronze)
    UNION ALL
    SELECT
        'Solar',
        (SELECT sum(rows) FROM system.parts
         WHERE database = 'solar' AND table = 'bronze' AND active),
        (SELECT max(date) FROM solar.bronze)
) sub
ORDER BY
    CASE source_name
        WHEN 'WSPR' THEN 1
        WHEN 'RBN' THEN 2
        WHEN 'PSK Reporter' THEN 3
        WHEN 'Contest' THEN 4
        WHEN 'Solar' THEN 5
    END
