-- Contest dataset aggregate statistics
-- contest.bronze columns: call_1 (logging station), call_2 (worked station), timestamp
SELECT
    (SELECT sum(rows) FROM system.parts
     WHERE database = 'contest' AND table = 'bronze' AND active) AS total_rows,
    (SELECT min(toDate(timestamp)) FROM contest.bronze) AS date_min,
    (SELECT max(toDate(timestamp)) FROM contest.bronze) AS date_max,
    (SELECT uniq(call_1) + uniq(call_2) FROM contest.bronze) AS unique_calls
