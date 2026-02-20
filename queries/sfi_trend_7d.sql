-- Daily SFI for the last 7 days from solar.bronze (GFZ Potsdam)
-- observed_flux = SFI (adjusted_flux is often 0 for recent days)
SELECT
    date,
    max(observed_flux) AS sfi
FROM solar.bronze
WHERE date >= today() - 7
  AND date < today()
  AND observed_flux > 0
GROUP BY date
ORDER BY date
