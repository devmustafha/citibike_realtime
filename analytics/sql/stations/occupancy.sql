SELECT station_id,
    num_bikes_available AS bikes_available,
    num_docks_available AS docks_available,
    ROUND(
        100.0 * num_bikes_available /
        NULLIF(num_bikes_available + num_docks_available, 0),
        2
    ) AS bike_occupancy_rate,
    last_reported_ts AS snapshot_time 
FROM latest_station_status;