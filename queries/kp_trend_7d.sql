-- Daily maximum Kp for the last 7 days from solar.bronze
SELECT
    date,
    max(kp_index) AS max_kp
FROM solar.bronze
WHERE date >= today() - 7
  AND date < today()
  AND kp_index >= 0
GROUP BY date
ORDER BY date
