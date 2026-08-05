SELECT
    snapshot_time,
    total_station_count,
    active_station_count,
    disabled_station_count,
    total_bikes_available,
    total_docks_available,
    bike_occupancy_rate
FROM system_metrics
ORDER BY snapshot_time DESC
LIMIT 1;