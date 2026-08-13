# Station Daily Metrics

## Business Requirement

- Provide a daily station-level summary of Citi Bike availability and occupancy.
- Support analysis of station performance across calendar days.
- Provide daily aggregates for longer-term station and system trend analysis.
- Identify station-days where data coverage is incomplete.
- Provide a stable Gold-layer dataset for downstream analytics and dashboard reporting.

## Grain

- One row per station per calendar day.
- Grain:
  - `station_id`
  - `year`
  - `month`
  - `day`

## Source

- Source dataset: Silver station status.
- Source fields:
  - `station_id`
  - `num_bikes_available`
  - `num_docks_available`
  - `last_reported_ts`
  - `year`
  - `month`
  - `day`
- The transformation processes one `process_date` at a time.

## Processing

- Filter Silver records to the requested `process_date`.
- Group records by `station_id`, `year`, `month`, and `day`.
- Calculate daily bike availability statistics.
- Calculate daily dock availability statistics.
- Count observations for each station-day.
- Calculate the average bike occupancy rate.
- Determine whether the station-day contains sufficient observations.

## Dimension

- `station_id`
  - Unique identifier for the Citi Bike station.
- `year`
  - Calendar year derived from `last_reported_ts`.
- `month`
  - Calendar month derived from `last_reported_ts`.
- `day`
  - Calendar day derived from `last_reported_ts`.

## Measures

- `min_bikes_available`
  - Minimum number of bikes available during the day.
- `max_bikes_available`
  - Maximum number of bikes available during the day.
- `avg_bikes_available`
  - Average number of bikes available during the day.
- `min_docks_available`
  - Minimum number of docks available during the day.
- `max_docks_available`
  - Maximum number of docks available during the day.
- `avg_docks_available`
  - Average number of docks available during the day.
- `avg_bike_occupancy_rate`
  - Ratio of average bikes available to total average station capacity.

## Quality Fields

- `observation_count`
  - Number of Silver station-status observations available for the station-day.
- `is_complete_day`
  - Indicates whether the station received more than 90% of expected observations.
- `is_complete_day` is calculated using:
  - `observation_count / EXPECTED_OBSERVATIONS_PER_DAY > 0.9`

## Transformation Logic

- Filter records where `year`, `month`, and `day` match `process_date`.
- Group by `station_id`, `year`, `month`, and `day`.
- Calculate minimum, maximum, and average bike availability.
- Calculate minimum, maximum, and average dock availability.
- Count source observations.
- Calculate `avg_bike_occupancy_rate` using:
  - `avg_bikes_available / (avg_bikes_available + avg_docks_available)`
- Cast `avg_bike_occupancy_rate` to `DecimalType(scale=2)`.
- Calculate `is_complete_day` from the observation count and expected daily observation count.

## Output

- Dataset: `station_daily_metrics`.
- Layer: Gold.
- Format: Parquet.
- Grain: one row per station per calendar day.
- Expected partition structure:

```text
station_daily_metrics/
└── year=YYYY/
    └── month=M/
        └── day=D/
            └── *.parquet