# station_hourly_metrics

## Overview

`station_hourly_metrics` is a Gold layer dataset that provides hourly aggregated metrics for every Citi Bike station. It is designed for analytics and operational reporting rather than serving raw event data.

---

## Business Requirement

Provide hourly station availability metrics so that operations and analytics teams can monitor station performance, identify trends, and understand bike and dock availability throughout the day.

Typical business questions include:

* How many bikes are typically available at each station every hour?
* Which stations frequently run out of bikes?
* Which stations remain consistently full?
* How does station availability change throughout the day?
* Which hours contain incomplete data and should be interpreted carefully?

---

## Grain

One row represents **one station during one hour**.

Example:

| station_id | hour                |
| ---------- | ------------------- |
| 72         | 2026-08-01 08:00:00 |
| 72         | 2026-08-01 09:00:00 |

---

## Source

**Input Dataset**

* Silver `station_status`

The Silver layer provides cleaned, deduplicated, and standardized station status events.

---

## Processing

* Processing Type: **Batch**
* Development Schedule: Every 30 minutes
* Production Schedule: Every hour (configurable)

---

## Dimensions

Each record is uniquely identified by:

* `station_id`
* `hour`

---

## Measures

The dataset contains the following aggregated metrics:

* `avg_bikes_available`
* `min_bikes_available`
* `max_bikes_available`
* `avg_docks_available`
* `min_docks_available`
* `max_docks_available`
* `avg_bike_occupancy_rate`
* `observation_count`

---

## Quality Fields

To improve transparency and data reliability, the dataset includes:

* `is_complete_hour`

This flag indicates whether the hourly aggregation contains the expected number of observations.

---

## Transformation Logic

1. Read Silver station status data.
2. Calculate `bike_occupancy_rate`.
3. Truncate `last_reported_ts` to the nearest hour.
4. Group records by:

   * `station_id`
   * `hour`
5. Calculate hourly aggregate metrics.
6. Determine whether the hour is complete.
7. Write the results to the Gold layer.

---

## Output

* Format: Parquet
* Layer: Gold
* Partition Strategy: *(To be decided during implementation.)*

---

## Validation Rules

The dataset should satisfy the following conditions:

* No duplicate `(station_id, hour)` records.
* `observation_count > 0`
* `min_bikes_available <= avg_bikes_available <= max_bikes_available`
* `min_docks_available <= avg_docks_available <= max_docks_available`
* `bike_occupancy_rate` must be between `0` and `1`, or `NULL` if total station capacity is zero.

---

## Assumptions

* The producer polls the Citi Bike API approximately once per minute.
* Silver data has already been cleaned and deduplicated.
* `last_reported_ts` is the event timestamp used for hourly aggregation.
* Missing observations may occur due to API outages or processing delays.
* Incomplete hours are retained and identified using `is_complete_hour`.

---

## Consumers

This dataset is intended for:

* Operational dashboards
* Trend analysis
* Business intelligence reporting
* Downstream Gold datasets (if required)

---

## Why This Dataset Exists

This dataset provides an analytics-ready hourly view of station availability without requiring downstream consumers to repeatedly aggregate Silver event data. It simplifies reporting, improves query performance, and exposes data quality information through the `is_complete_hour` indicator.
