SELECT 
    hour, 
    (AVG(avg_bike_occupancy_rate)::DECIMAL(3,2)) as avg_occupancy_rate
FROM station_hourly_metrics
GROUP BY hour
ORDER BY hour;