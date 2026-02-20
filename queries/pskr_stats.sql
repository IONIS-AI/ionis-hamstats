-- PSK Reporter dataset aggregate statistics
-- pskr.bronze columns: sender_call (TX), receiver_call (RX), timestamp
SELECT
    (SELECT sum(rows) FROM system.parts
     WHERE database = 'pskr' AND table = 'bronze' AND active) AS total_rows,
    (SELECT min(toDate(timestamp)) FROM pskr.bronze) AS date_min,
    (SELECT max(toDate(timestamp)) FROM pskr.bronze
     WHERE timestamp >= now() - INTERVAL 7 DAY) AS date_max,
    (SELECT dateDiff('day',
        min(toDate(timestamp)),
        max(toDate(timestamp))) + 1
     FROM pskr.bronze) AS days_collected,
    (SELECT uniq(sender_call) FROM pskr.bronze) AS unique_tx_calls,
    (SELECT uniq(receiver_call) FROM pskr.bronze) AS unique_rx_calls
