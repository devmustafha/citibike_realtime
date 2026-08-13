# Latest Station Status

## Business Requirement

- Provide the most recent known status for every Citi Bike station.
- Support real-time or near-real-time station availability monitoring.
- Provide the primary station-level dataset for the dashboard's current-status views.
- Allow users to identify stations with available bikes and available docks.
- Provide the latest station snapshot without requiring downstream consumers to process the full Silver history.

## Grain

- One row per station representing the latest available station-status observation.
- Grain:
  - `station_id`

## Source

- Source dataset: Silver station status.
- Source fields:
  - `station_id`
  - `num_bikes_available`
  - `num_docks_available`
  - `last_reported_ts`
- The dataset is derived by selecting the most recent observation for each station.

## Processing

- Read cleaned station status records from the Silver layer.
- Group observations by `station_id`.
- Identify the most recent observation for each station using `last_reported_ts`.
- Retain the bike and dock availability values from the latest observation.
- Calculate the current bike occupancy rate.
- Expose the latest observation timestamp for freshness monitoring.

## Dimension

- `station_id`
  - Unique identifier for the Citi Bike station.

## Measures

- `num_bikes_available`
  - Number of bikes currently available at the station.
- `num_docks_available`
  - Number of docks currently available at the station.
- `bike_occupancy_rate`
  - Proportion of station capacity currently occupied by bikes.

## Quality Fields

- `last_reported_ts`
  - Timestamp of the latest station-status observation.
- The timestamp allows downstream consumers to determine how fresh the station status is.
- A station with an older `last_reported_ts` may indicate delayed or missing source data.

## Transformation Logic

- Identify the latest observation for each `station_id`.
- Use `last_reported_ts` to determine the most recent record.
- Retain:
  - `station_id`
  - `num_bikes_available`
  - `num_docks_available`
  - `last_reported_ts`
- Calculate `bike_occupancy_rate` using:

```text
100.0 * num_bikes_available /
NULLIF(
    num_bikes_available + num_docks_available,
    0
)