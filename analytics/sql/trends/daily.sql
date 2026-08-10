SELECT
    MAKE_DATE(year, month, day) AS date,

    ROUND(AVG(avg_bikes_available), 2) AS avg_bikes_available,
    ROUND(AVG(avg_docks_available), 2) AS avg_docks_available,

    ROUND(
        100.0 * AVG(avg_bikes_available)
        / NULLIF(
            AVG(avg_bikes_available) + AVG(avg_docks_available),
            0
        ),
        2
    ) AS avg_occupancy_rate,

    ROUND(
        MAX(
            100.0 * max_bikes_available
            / NULLIF(max_bikes_available + min_docks_available, 0)
        ),
        2
    ) AS peak_occupancy_rate,

    ROUND(
        MIN(
            100.0 * min_bikes_available
            / NULLIF(min_bikes_available + max_docks_available, 0)
        ),
        2
    ) AS lowest_occupancy_rate

FROM station_daily_metrics
GROUP BY year, month, day
ORDER BY year, month, day;