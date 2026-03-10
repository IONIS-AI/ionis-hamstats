-- Operator categories — power, operator class, assisted/non-assisted
-- Three result sets combined with UNION ALL for single query
SELECT 'power' AS category, category_power AS value, count() AS logs,
       round(count() * 100.0 / sum(count()) OVER (), 2) AS pct
FROM contest.log_metadata
WHERE category_power != ''
GROUP BY category_power
UNION ALL
SELECT 'operator' AS category, category_operator AS value, count() AS logs,
       round(count() * 100.0 / sum(count()) OVER (), 2) AS pct
FROM contest.log_metadata
WHERE category_operator != ''
GROUP BY category_operator
UNION ALL
SELECT 'assisted' AS category, category_assisted AS value, count() AS logs,
       round(count() * 100.0 / sum(count()) OVER (), 2) AS pct
FROM contest.log_metadata
WHERE category_assisted != ''
GROUP BY category_assisted
ORDER BY category, logs DESC
