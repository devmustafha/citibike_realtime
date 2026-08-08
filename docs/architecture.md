# System Architecture

## 1. Overview

The Citi Bike Real-Time Data Engineering Pipeline is designed to ingest Citi Bike station-status data continuously, process it through a medallion-style data architecture, and produce analytical datasets for downstream querying.

The system combines real-time streaming with scheduled batch processing.

The architecture is divided into two major workloads:

* **Streaming workloads** — ingestion and data refinement.
* **Batch workloads** — analytical Gold-layer processing.

```text
                         Citi Bike GBFS API
                                │
                                ▼
                         Python Producer
                                │
                                ▼
                              Kafka
                                │
                                ▼
                     Bronze Structured Stream
                                │
                                ▼
                     Silver Structured Stream
                                │
                ┌───────────────┴────────────────┐
                │                                │
                ▼                                ▼
       Station Hourly Gold              Station Daily Gold
          Airflow + Spark                  Airflow + Spark
                │                                │
                └───────────────┬────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            Latest Station Status      System Metrics
                    │                       │
                    └───────────┬───────────┘
                                ▼
                             DuckDB
                                │
                                ▼
                            Analytics
```

---

## 2. Architecture Principles

The project follows several key architectural principles:

### Separation of streaming and batch workloads

Continuous workloads are handled by Spark Structured Streaming, while finite analytical workloads are orchestrated by Airflow.

### Layered data architecture

Data progresses through:

```text
Bronze → Silver → Gold
```

Each layer has a distinct responsibility.

### Idempotent analytical processing

Gold jobs process an explicit date and use dynamic partition overwrite so that retries replace existing partitions rather than creating duplicates.

### Configuration outside application logic

Application configuration is centralized through Pydantic Settings and environment variables.

### Failure visibility

Airflow retries failed tasks and sends Telegram notifications when tasks ultimately fail.

---

# 3. Components

## 3.1 Citi Bike API

The Citi Bike GBFS station-status endpoint provides the source data.

The feed contains information such as:

* station ID
* available bikes
* available docks
* available e-bikes
* installation status
* rental status
* return status
* last reported timestamp

The producer periodically retrieves this feed.

---

## 3.2 Python Producer

The producer is responsible for ingestion.

Its responsibilities are:

1. Request the Citi Bike station-status feed.
2. Validate the response using Pydantic.
3. Extract individual station records.
4. Publish each station record to Kafka.

The flow is:

```text
Citi Bike API
      ↓
HTTPX
      ↓
Pydantic validation
      ↓
StationStatus objects
      ↓
Kafka producer
```

The producer is intentionally separated from downstream processing.

This allows the ingestion process and processing infrastructure to operate independently.

---

# 4. Kafka

Kafka provides the streaming boundary between ingestion and processing.

The producer publishes station-status records to:

```text
station-status
```

Kafka allows the producer to operate independently of Spark.

If Spark temporarily stops processing, Kafka can retain messages until downstream processing resumes, subject to the configured Kafka retention policy.

The internal Docker network uses:

```text
kafka:9092
```

while the externally exposed development listener uses:

```text
localhost:29092
```

---

# 5. Bronze Layer

The Bronze layer is the first Spark Structured Streaming stage.

Its primary responsibility is to persist incoming station-status events with minimal transformation.

```text
Kafka
  ↓
Spark Structured Streaming
  ↓
Bronze Parquet
```

The Bronze layer acts as a durable representation of the incoming stream.

A Spark checkpoint is used to track streaming progress and support recovery.

The Bronze layer intentionally performs minimal business transformation so that the original event data remains available for downstream processing.

---

# 6. Silver Layer

The Silver layer consumes Bronze data and produces cleaned, standardized records.

The transformation performs:

* validation of required station fields
* removal of invalid rows
* Unix timestamp conversion
* creation of date-partition columns

The timestamp transformation converts:

```text
last_reported
```

from a Unix timestamp into:

```text
last_reported_ts
```

The Silver layer also derives:

```text
year
month
day
```

The resulting data is partitioned by date.

```text
Bronze
   ↓
Validation
   ↓
Timestamp standardization
   ↓
Date derivation
   ↓
Silver
```

Like Bronze, Silver is a continuously running Structured Streaming workload.

---

# 7. Gold Layer

Gold contains analytical datasets rather than raw or cleaned events.

The Gold layer currently contains:

```text
latest_station_status
station_hourly
station_daily
system_metrics
```

Gold processing is performed as finite Spark batch jobs.

Airflow orchestrates these jobs.

---

## 7.1 Station Hourly Metrics

The hourly job receives a processing date.

It filters Silver data to that date:

```text
year = process_date.year
month = process_date.month
day = process_date.day
```

The data is then grouped by:

```text
station_id
year
month
day
hour
```

The job calculates:

* minimum bikes
* maximum bikes
* average bikes
* minimum docks
* maximum docks
* average docks
* observation count
* average bike occupancy rate
* hourly completeness

The output is partitioned by:

```text
year/month/day/hour
```

---

## 7.2 Station Daily Metrics

The daily job follows the same approach but aggregates an entire day.

Records are grouped by:

```text
station_id
year
month
day
```

The job calculates:

* minimum bikes
* maximum bikes
* average bikes
* minimum docks
* maximum docks
* average docks
* observation count
* average bike occupancy rate
* daily completeness

The output is partitioned by:

```text
year/month/day
```

---

## 7.3 Occupancy Rate

The Gold layer calculates bike occupancy using average availability:

```text
                   avg_bikes_available
occupancy = ───────────────────────────────────────
            avg_bikes_available + avg_docks_available
```

The metric is intentionally calculated in Gold because it is an analytical/business metric rather than a raw station-status attribute.

If the denominator is zero, occupancy is represented as `NULL`.

This distinguishes unavailable occupancy from genuine zero occupancy.

---

## 7.4 Completeness

Gold metrics include completeness indicators.

For hourly data:

```text
observation_count
──────────────────────── > 0.9
expected hourly count
```

For daily data:

```text
observation_count
──────────────────────── > 0.9
expected daily count
```

This allows downstream analytics to identify periods where insufficient observations were available.

---

# 8. Latest Station Status

The latest station-status job produces a current snapshot of station conditions.

Unlike historical hourly and daily metrics, this dataset represents the latest known state.

It is therefore treated as a snapshot rather than a historical aggregation.

---

# 9. System Metrics

System metrics provide aggregated information about the overall Citi Bike system.

The system metrics job is executed together with the latest station-status workflow.

This allows the project to expose both:

* station-level current status
* system-level analytical information

---

# 10. Airflow

Airflow orchestrates the finite Gold workloads.

Current DAGs include:

```text
latest_station_status
station_hourly_metrics
station_daily_metrics
```

The latest station-status DAG also executes the system metrics job.

The general flow is:

```text
Airflow
   ↓
BashOperator
   ↓
run_spark_job.sh
   ↓
spark-submit
   ↓
Spark Gold application
```

Airflow passes the processing date to Gold jobs.

This makes the jobs deterministic and supports safe retries and backfills.

---

# 11. Why Bronze and Silver Are Not Airflow DAGs

Bronze and Silver are continuously running Spark Structured Streaming applications.

They are designed to remain active rather than start, process a finite dataset, and terminate.

Therefore:

```text
Bronze/Silver
    ↓
Long-running streaming processes
    ↓
Managed by Spark/Docker
```

while:

```text
Gold
    ↓
Finite batch processing
    ↓
Managed by Airflow
```

This separation prevents Airflow tasks from remaining permanently in a `running` state.

---

# 12. Idempotency

Gold processing is designed to be idempotent.

Each Gold job receives an explicit processing date.

For example:

```text
--process-date 2026-08-07
```

The hourly job processes only:

```text
2026-08-07
```

and the daily job processes only:

```text
2026-08-07
```

Gold data is partitioned according to its natural grain.

Hourly:

```text
year/month/day/hour
```

Daily:

```text
year/month/day
```

The shared Gold I/O layer uses dynamic partition overwrite.

Therefore, if an Airflow task is retried, the existing partitions for that processing period are replaced instead of new duplicate records being appended.

---

# 13. Storage

MinIO provides S3-compatible object storage for the project.

The logical storage structure is:

```text
s3a://bronze/
s3a://silver/
s3a://gold/
```

Parquet is used as the primary storage format.

Partitioning improves organization and allows downstream processing to work with specific periods of data.

---

# 14. DuckDB

DuckDB provides the analytical query layer.

It can query the Gold Parquet datasets directly without requiring a separate analytical database.

Conceptually:

```text
Gold Parquet
     ↓
   DuckDB
     ↓
   Views
     ↓
 Analytics
```

This provides a lightweight analytical interface for exploring the processed data.

---

# 15. Docker

Docker Compose provides the local infrastructure environment.

The major services are:

```text
minio
kafka
kafka-ui
spark-master
spark-worker
airflow-init
airflow-webserver
airflow-scheduler
postgres
```

Docker provides reproducibility by allowing the infrastructure to be started consistently across development environments.

---

# 16. Configuration

Configuration is centralized through Pydantic Settings.

The application reads configuration using:

```python
settings = get_settings()
```

Configuration includes:

* API URL
* Kafka configuration
* storage paths
* MinIO configuration
* Telegram configuration

Secrets are supplied through environment variables rather than being embedded in application code.

---

# 17. Failure Handling

The project implements multiple levels of failure recovery.

### Streaming recovery

Spark Structured Streaming checkpoints allow streaming applications to resume processing after failures.

### Airflow retries

Gold tasks can be retried automatically.

### Telegram notifications

When an Airflow task ultimately fails, the failure callback sends a Telegram notification.

The operational flow is:

```text
Task failure
     ↓
Airflow retry
     ↓
Retry fails
     ↓
Task marked FAILED
     ↓
Telegram notification
```

---

# 18. CI/CD

GitHub Actions validates both application code and Docker infrastructure.

The quality job runs:

```text
uv sync --locked
        ↓
Ruff format
        ↓
Ruff lint
        ↓
pytest
```

The Docker job runs:

```text
docker compose config
        ↓
Airflow image build
        ↓
Spark image build
```

This ensures that changes are checked before they are merged.

---

# 19. Repository Architecture

The project is organized around the responsibilities of each pipeline layer.

```text
producer/
    Ingestion

bronze/
    Streaming ingestion

silver/
    Streaming transformation

gold/
    Analytical processing

airflow/
    Orchestration

common/
    Shared configuration, sessions,
    storage, and utilities

docker/
    Infrastructure image definitions

tests/
    Automated tests

scripts/
    Operational scripts
```

---

# 20. End-to-End Data Flow

The complete system can be summarized as:

```text
                         ┌──────────────────┐
                         │  Citi Bike API   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Python Producer  │
                         │ HTTPX + Pydantic │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Kafka       │
                         │ station-status   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Bronze Streaming │
                         │      Spark       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Silver Streaming │
                         │      Spark       │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼──────────────┐
                    │             │              │
                    ▼             ▼              ▼
                Hourly         Daily          Latest
                 Gold           Gold          Snapshot
                    │             │              │
                    └─────────────┼──────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      DuckDB      │
                         │     Analytics    │
                         └──────────────────┘

                 Airflow orchestrates Gold jobs
                 Docker manages infrastructure
                 Telegram handles failure alerts
```

---

# 21. Summary

The architecture intentionally combines streaming and batch processing:

```text
Streaming:
API → Producer → Kafka → Bronze → Silver

Batch:
Silver → Airflow → Spark Gold → DuckDB
```

This separation provides:

* decoupled ingestion
* continuous processing
* durable intermediate storage
* analytical data products
* scheduled computation
* retryable processing
* idempotent Gold writes
* failure notifications
* reproducible local infrastructure
* automated code and Docker validation

The result is a complete end-to-end real-time data engineering pipeline suitable for demonstrating practical data engineering architecture and operational concepts.
