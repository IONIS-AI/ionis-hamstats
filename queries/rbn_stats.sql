-- RBN dataset aggregate statistics
SELECT
    (SELECT sum(rows) FROM system.parts
     WHERE database = 'rbn' AND table = 'bronze' AND active) AS total_rows,
    (SELECT min(toDate(timestamp)) FROM rbn.bronze
     WHERE timestamp > '2008-01-01') AS date_min,
    (SELECT max(toDate(timestamp)) FROM rbn.bronze
     WHERE timestamp >= now() - INTERVAL 7 DAY) AS date_max,
    (SELECT uniq(dx_call) FROM rbn.bronze) AS unique_tx_calls,
    (SELECT uniq(de_call) FROM rbn.bronze) AS unique_rx_calls
