-- WSPR dataset aggregate statistics
-- wspr.bronze columns: callsign (TX), reporter (RX), timestamp
SELECT
    (SELECT sum(rows) FROM system.parts
     WHERE database = 'wspr' AND table = 'bronze' AND active) AS total_rows,
    (SELECT min(toDate(timestamp)) FROM wspr.bronze
     WHERE timestamp > '2007-01-01') AS date_min,
    (SELECT max(toDate(timestamp)) FROM wspr.bronze
     WHERE timestamp >= now() - INTERVAL 7 DAY) AS date_max,
    (SELECT uniq(callsign) FROM wspr.bronze) AS unique_tx_calls,
    (SELECT uniq(reporter) FROM wspr.bronze) AS unique_rx_calls
