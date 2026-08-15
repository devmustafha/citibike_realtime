# Station Information

## Business Requirement

- Provide a reliable, daily snapshot of Citi Bike station metadata.
- Capture relatively static information about each station, including:
  - Station identifier.
  - Station name.
  - Station location.
  - Station capacity and related station attributes.
- Keep station metadata separate from frequently changing station-status data.
- Make station information available for enriching downstream analytical datasets such as hourly and daily station metrics.

## Grain

- One record represents **one station at a point in time**.
- A daily ingestion produces a snapshot of the available station information.
- The natural business key is:
  - `station_id`
  - `snapshot_date`

## Source

- **Source:** Citi Bike GBFS `station_information` endpoint.
- Data is retrieved through the Citi Bike API client.
- The dataset is ingested as a **batch process once per day**.
- Unlike `station_status`, station information is not treated as streaming data because the attributes change relatively infrequently.

## Processing

- Fetch the latest station information from the Citi Bike API.
- Validate that the API is reachable before processing.
- Extract the station records from the API response.
- Validate the response structure.
- Convert the API response into a Spark DataFrame.
- Apply the station information schema.
- Add ingestion and snapshot metadata.
- Write the resulting dataset to the designated bucket location.
- Make the data available for downstream Silver-layer processing.

## Dimension

- `station_id`
  - Unique Citi Bike station identifier.
- `station_name`
  - Human-readable station name.
- `latitude`
  - Station latitude.
- `longitude`
  - Station longitude.
- `capacity`
  - Total station capacity where provided.
- `short_name`
  - Short station identifier where provided.
- `station_type`
  - Type of station where provided.

## Measures

- `capacity`
  - Represents the reported station capacity where provided.
- No operational availability measures are calculated in this dataset.
- Current bike and dock availability belong to the `station_status` dataset.

## Quality Fields

- `snapshot_date`
  - Date on which the station information was retrieved.
- `ingested_at`
  - Timestamp at which the record was ingested.
- `source`
  - Identifies Citi Bike GBFS as the source.
- `year`
  - Partition year derived from `snapshot_date`.
- `month`
  - Partition month derived from `snapshot_date`.
- `day`
  - Partition day derived from `snapshot_date`.

## Transformation Logic

- Retrieve station information from the Citi Bike `station_information` API.
- Extract the `stations` array from the API response.
- Apply the predefined station information schema.
- Preserve source station attributes without unnecessary transformations.
- Normalize data types where required.
- Generate `snapshot_date` from the ingestion date.
- Generate `ingested_at` from the ingestion timestamp.
- Derive `year`, `month`, and `day` from `snapshot_date`.
- Remove duplicate station records for the same snapshot date.
- Retain one record per `station_id` per `snapshot_date`.
- Do not join with `station_status` during ingestion.
- Station-status metrics are enriched downstream using `station_id`.

## Output

- **Format:** Parquet.
- **Storage:** S3-compatible object storage / MinIO.
- **Dataset:** `station_information`.
- Data is partitioned by:
  - `year`
  - `month`
  - `day`

Example:

```text
station_information/
├── year=2026/
│   ├── month=08/
│   │   ├── day=15/
│   │   │   └── part-*.parquet
│   │   └── ...
│   └── ...
└── ...
```

- The dataset represents the station metadata available at each daily snapshot.

## Validation Rules

- `station_id` must not be null.
- `station_id` must be unique within a given `snapshot_date`.
- `station_name` should not be null where provided by the source.
- `latitude` must contain a valid geographic latitude.
- `longitude` must contain a valid geographic longitude.
- `capacity`, when provided, must be non-negative.
- `snapshot_date` must not be null.
- `ingested_at` must not be null.
- The API response must contain a valid station collection.
- Records failing required-field validation should not be written to the trusted downstream dataset.
- The ingestion should fail or raise an appropriate error when the Citi Bike API is unavailable.

## Assumptions

- Station information changes less frequently than station status.
- A daily snapshot is sufficient to capture meaningful station metadata changes.
- `station_id` remains the stable identifier used to associate station information with station-status records.
- The Citi Bike API remains the authoritative source for station metadata.
- Missing optional attributes are represented as `NULL` rather than fabricated default values.
- Historical snapshots are retained rather than overwriting previous station information.
- Station information does not require Kafka because it is not a continuously streaming dataset.
- The daily ingestion process can be scheduled independently from the station-status streaming pipeline.

## Consumers

- **Silver station information dataset**
  - Cleans and standardizes the raw station metadata.
- **Station hourly metrics**
  - Uses station information to enrich hourly station-status metrics.
- **Station daily metrics**
  - Uses station metadata to provide station-level context.
- **Latest station status**
  - Can use station information to attach descriptive station attributes.
- **Analytics/dashboard**
  - Uses station names, locations, capacity, and other metadata for reporting and visualization.

## Why This Dataset Exists

- Separates relatively static station metadata from frequently changing station-status data.
- Provides a historical record of station configuration over time.
- Prevents downstream datasets from repeatedly calling the external Citi Bike API.
- Provides a reliable historical dimension that can be joined to operational station-status data.
- Allows analysts to understand what a station was configured like at a particular point in time, rather than only its current configuration.
- Provides the foundation for enriching Gold-layer station metrics with descriptive station attributes.