SELECT 
    station_id,
    ROUND(AVG(avg_bike_occupancy_rate), 2) AS avg_occupancy_rate,
    ROUND(AVG(avg_bikes_available), 0) AS avg_bikes_available,
    ROUND(AVG(avg_docks_available), 0) AS avg_docks_available,
    RANK() OVER (
        ORDER BY AVG(avg_bike_occupancy_rate) DESC
    ) AS station_rank
FROM station_daily_metrics
GROUP BY station_id
ORDER BY station_rank;