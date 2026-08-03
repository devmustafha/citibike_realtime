# System Metrics

## Business Requirement

Provide a system-level dataset that summarizes the current state of the Citi Bike network at a specific point in time. This dataset enables operations teams and business stakeholders to monitor network health, capacity, and utilization through high-level metrics without querying individual stations.

---

## Grain

**One row represents the state of the entire Citi Bike network at a single point in time (snapshot).**

---

## Source

**Input Dataset:** `gold/latest_station_status`

### Rationale

The `latest_station_status` dataset already contains the most recent record for each station. Since the objective is to represent the current state of the network, using this dataset:

- Eliminates the need to process historical observations.
- Avoids repeating "latest record" logic.
- Promotes reuse of trusted Gold datasets.
- Reduces processing time and computational cost.

---

## Processing Frequency

The dataset is refreshed according to business demand:

- **Rush hour:** Every 15 minutes
- **Off-peak hours:** Every 30 minutes

This provides a balance between data freshness and processing cost while ensuring operational dashboards remain sufficiently up to date.

Each snapshot includes a `snapshot_time` to indicate when the metrics were calculated.

---

## Processing Type

**Batch (scheduled)**

Since the dataset provides periodic operational summaries rather than real-time analytics, scheduled batch processing is sufficient and more cost-effective than continuous streaming.

---

## Dimensions

| Column | Description |
|---------|-------------|
| snapshot_time | Timestamp representing when the network snapshot was generated. |

---

## Measures

| Metric | Description |
|--------|-------------|
| total_bikes_available | Total number of bikes currently available across all stations. |
| total_docks_available | Total number of empty docks currently available across all stations. |
| active_station_count | Number of stations currently active. |
| disabled_station_count | Number of stations currently unavailable or disabled. |
| total_station_count | Total number of stations in the network. |

---

## Derived Metrics

| Metric | Formula |
|--------|---------|
| bike_occupancy_rate | `total_bikes_available / (total_bikes_available + total_docks_available)` |

---

## Data Quality

Since this dataset consumes the trusted `latest_station_status` Gold dataset, data cleaning is expected to have already been performed upstream.

The following validation checks ensure the aggregated metrics remain trustworthy:

- Source dataset contains at least one record.
- No aggregate metric contains negative values.
- `bike_occupancy_rate` is between **0** and **1**.
- Exactly one row exists for each `snapshot_time`.

---

## Partition Strategy

The dataset is partitioned by:

- `year`
- `month`
- `day`

derived from `snapshot_time`.

### Rationale

- Enables efficient date-based queries.
- Supports partition pruning.
- Maintains consistency with the Bronze and Silver layers.
- Avoids over-partitioning while allowing the dataset to scale over time.

---

## Consumers

Primary consumers include:

- Data Analysts
- Business Intelligence Teams
- Operations Teams

---

## Validation

The following validation checks should pass before publishing the dataset:

- `total_bikes_available` equals the sum of `num_bikes_available` from `latest_station_status`.
- `total_docks_available` equals the sum of `num_docks_available` from `latest_station_status`.
- `active_station_count + disabled_station_count = total_station_count`.
- `bike_occupancy_rate` is within the range **[0, 1]**.
- `snapshot_time` is unique.
- The dataset contains exactly one row for each generated snapshot.

---

## Expected Workflow

```
Latest Station Status
        │
        ▼
Read Snapshot
        │
        ▼
Aggregate Network Metrics
        │
        ▼
Calculate Derived Metrics
        │
        ▼
Run Validation Checks
        │
        ▼
Write Gold Dataset
```