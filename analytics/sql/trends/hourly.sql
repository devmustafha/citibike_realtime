SELECT
    hour,

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

    COUNT(DISTINCT station_id) AS reporting_stations

FROM station_hourly_metrics
GROUP BY hour
ORDER BY hour;