SELECT 
    snapshot_time,
    total_bikes_available,
    total_docks_available,
    bike_occupancy_rate
FROM system_metrics
ORDER BY snapshot_time DESC
LIMIT 1;