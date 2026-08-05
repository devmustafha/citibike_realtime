SELECT
    station_id,

    -- Bike availability
    ROUND(AVG(avg_bikes_available), 2) AS avg_bikes_available,
    MIN(min_bikes_available) AS lowest_bikes_available,
    MAX(max_bikes_available) AS highest_bikes_available,

    -- Dock availability
    ROUND(AVG(avg_docks_available), 2) AS avg_docks_available,
    MIN(min_docks_available) AS lowest_docks_available,
    MAX(max_docks_available) AS highest_docks_available,

    -- Average occupancy
    ROUND(
        100.0 * AVG(avg_bikes_available)
        / NULLIF(
            AVG(avg_bikes_available) + AVG(avg_docks_available),
            0
        ),
        2
    ) AS avg_occupancy_rate,

    -- Occupancy variability
    ROUND(
        VAR_SAMP(
            100.0 * avg_bikes_available
            / NULLIF(avg_bikes_available + avg_docks_available, 0)
        ),
        2
    ) AS occupancy_variance,

    ROUND(
        STDDEV_SAMP(
            100.0 * avg_bikes_available
            / NULLIF(avg_bikes_available + avg_docks_available, 0)
        ),
        2
    ) AS occupancy_stddev,

    -- Number of days observed
    COUNT(*) AS observation_days

FROM station_daily_metrics
GROUP BY station_id
ORDER BY avg_occupancy_rate DESC;