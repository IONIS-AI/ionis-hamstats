-- Current solar conditions from NOAA SWPC live feed
SELECT
    solar_flux,
    kp_index,
    conditions
FROM wspr.live_conditions
LIMIT 1
