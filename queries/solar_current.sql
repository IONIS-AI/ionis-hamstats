-- Current solar conditions from NOAA SWPC live feed.
--
-- ORDER BY updated_at DESC LIMIT 1 is load-bearing. wspr.live_conditions was an
-- ENGINE = Memory table holding exactly one row, so a bare LIMIT 1 was unambiguous.
-- It is now a durable append-only MergeTree at 15-minute resolution, where LIMIT 1
-- returns an ARBITRARY row -- a plausible set of solar indices from some point in
-- the last two years, indistinguishable from current ones.
--
-- The observation timestamps come back too: a consumer that cannot ask how old a
-- reading is cannot tell a measurement from a leftover.
SELECT
    solar_flux,
    kp_index,
    ap_index,
    conditions,
    sfi_observed_at,
    kp_observed_at,
    updated_at
FROM wspr.live_conditions
ORDER BY updated_at DESC
LIMIT 1
