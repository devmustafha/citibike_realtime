# Citi Bike Real-Time Data Engineering Pipeline

A real-time data engineering pipeline for ingesting, processing, and analyzing Citi Bike station-status data using Kafka, Apache Spark, MinIO, Airflow, DuckDB, and Python.

The project demonstrates a complete modern data-engineering workflow, from real-time API ingestion through streaming processing and analytical data products.

---

## Architecture

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

### Streaming vs batch

The project deliberately separates continuous streaming workloads from finite analytical workloads.

**Streaming layer**

* Citi Bike API
* Python producer
* Kafka
* Bronze Spark Structured Streaming
* Silver Spark Structured Streaming

**Batch/analytical layer**

* Airflow
* Spark Gold jobs
* DuckDB analytical views

Airflow does **not** manage the Bronze and Silver streams because those jobs are intended to run continuously. Airflow instead orchestrates finite Gold processing jobs.

---

## Data Architecture

The pipeline follows a simplified medallion architecture.

### Bronze

Bronze contains the raw station-status data received from Kafka.

The objective is to preserve the incoming data while storing it in an analytics-friendly format.

```text
Kafka
  ↓
Bronze
  ↓
Parquet
```

### Silver

Silver cleans and standardizes the Bronze data.

The transformation includes:

* removing records without a station ID
* removing records without `last_reported`
* converting Unix timestamps to Spark timestamps
* deriving `year`, `month`, and `day`
* partitioning the data by date

Conceptually:

```text
Bronze
   ↓
Validation
   ↓
Timestamp conversion
   ↓
Date derivation
   ↓
Silver Parquet
```

### Gold

Gold contains analytical datasets designed for querying and reporting.

The project currently produces:

* latest station status
* station hourly metrics
* station daily metrics
* system metrics

---

## Gold Metrics

### Station hourly metrics

Hourly metrics are calculated for every station.

Each metric is identified by:

```text
station_id
year
month
day
hour
```

The dataset contains:

* minimum bikes available
* maximum bikes available
* average bikes available
* minimum docks available
* maximum docks available
* average docks available
* observation count
* average bike occupancy rate
* hourly completeness indicator

Hourly data is partitioned by:

```text
year/month/day/hour
```

### Station daily metrics

Daily metrics are calculated for every station.

Each metric is identified by:

```text
station_id
year
month
day
```

The dataset contains:

* minimum bikes available
* maximum bikes available
* average bikes available
* minimum docks available
* maximum docks available
* average docks available
* observation count
* average bike occupancy rate
* daily completeness indicator

Daily data is partitioned by:

```text
year/month/day
```

### Bike occupancy

Bike occupancy is calculated as:

```text
average bikes available
────────────────────────────────────────────
average bikes available + average docks available
```

If the denominator is zero, occupancy is represented as `NULL` rather than `0`.

This distinguishes:

```text
0% occupancy
```

from:

```text
occupancy unavailable
```

---

## Data Completeness

The Gold layer includes completeness indicators.

For hourly metrics:

```text
observation_count / expected_observations_per_hour > 0.9
```

For daily metrics:

```text
observation_count / expected_observations_per_day > 0.9
```

This allows downstream analytics to distinguish complete periods from periods with insufficient observations.

---

## Technology Stack

| Technology                 | Purpose                              |
| -------------------------- | ------------------------------------ |
| Python                     | API producer and application logic   |
| Pydantic                   | Data validation                      |
| HTTPX                      | Citi Bike API client                 |
| Apache Kafka               | Real-time messaging                  |
| Apache Spark               | Streaming and distributed processing |
| Spark Structured Streaming | Bronze/Silver streaming              |
| MinIO                      | S3-compatible object storage         |
| Apache Airflow             | Gold-job orchestration               |
| DuckDB                     | Analytical querying                  |
| Parquet                    | Data storage format                  |
| Docker Compose             | Local infrastructure                 |
| pytest                     | Testing                              |
| Ruff                       | Formatting and linting               |
| uv                         | Python dependency management         |
| GitHub Actions             | CI                                   |

---

## Project Structure

```text
.
├── airflow/
│   ├── dags/
│   ├── logs/
│   └── plugins/
│
├── common/
│   ├── config.py
│   ├── logging.py
│   ├── session.py
│   ├── storage.py
│   └── ...
│
├── producer/
│   ├── client.py
│   ├── main.py
│   └── models.py
│
├── bronze/
│   └── ingest_station_status.py
│
├── silver/
│   ├── main.py
│   └── transform.py
│
├── gold/
│   ├── io.py
│   ├── latest_station_status/
│   ├── station_hourly_metrics/
│   ├── station_daily_metrics/
│   └── system_metrics/
│
├── scripts/
│   └── run_spark_job.sh
│
├── docker/
│   ├── airflow/
│   └── spark/
│
├── tests/
│
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Configuration

Application configuration is centralized through Pydantic Settings.

The application loads configuration lazily through `get_settings()`.

Example configuration:

```env
CITIBIKE_API_URL=...
KAFKA_BOOTSTRAP_SERVERS=...
BRONZE_STATION_STATUS_PATH=...
SILVER_STATION_STATUS_PATH=...
SILVER_STATION_CHECKPOINT_PATH=...

MINIO_ENDPOINT=...
MINIO_ACCESS_KEY=...
MINIO_SECRET_KEY=...
MINIO_SECURE=false

TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

Non-secret defaults such as Kafka topics and Gold paths can remain defined in `Settings`.

Secrets should never be committed to the repository.

Use `.env.example` to document required variables without exposing credentials.

---

## Running the Project

### 1. Configure environment variables

Create a local `.env` file containing the required configuration.

Never commit this file.

### 2. Build the infrastructure

```bash
docker compose build
```

### 3. Start the infrastructure

```bash
docker compose up -d
```

The stack includes:

* MinIO
* Kafka
* Kafka UI
* Spark master
* Spark worker
* Airflow
* PostgreSQL

### 4. Verify containers

```bash
docker compose ps
```

### 5. Monitor services

Airflow:

```text
http://localhost:8088
```

Spark:

```text
http://localhost:8081
```

MinIO:

```text
http://localhost:9001
```

Kafka UI:

```text
http://localhost:8080
```

---

## Streaming Pipeline

The producer periodically retrieves Citi Bike station-status data.

```text
Citi Bike API
     ↓
CitiBikeClient
     ↓
Pydantic validation
     ↓
KafkaProducer
     ↓
station-status topic
```

Bronze consumes the Kafka topic using Spark Structured Streaming.

Silver consumes Bronze and applies cleaning and standardization.

The streaming jobs are intentionally long-running and are therefore managed by the Docker/Spark infrastructure rather than Airflow.

---

## Airflow

Airflow orchestrates the finite Gold processing jobs.

Current DAGs include:

```text
latest_station_status
station_hourly_metrics
station_daily_metrics
```

The latest station status DAG also runs the system metrics job.

Gold jobs receive their processing date from Airflow and pass it to Spark.

For example:

```text
Airflow logical date
        ↓
--process-date YYYY-MM-DD
        ↓
Spark Gold job
        ↓
Process only that date
```

This makes backfills and retries deterministic.

---

## Idempotency

Gold processing is designed to be idempotent.

Hourly data is partitioned by:

```text
year/month/day/hour
```

Daily data is partitioned by:

```text
year/month/day
```

Gold writes use dynamic partition overwrite.

Therefore, rerunning the same processing date replaces the relevant partitions rather than appending duplicate records.

Conceptually:

```text
First run
2026-08-07
    ↓
write 2026-08-07 partitions

Retry
2026-08-07
    ↓
replace 2026-08-07 partitions
```

Other dates remain unaffected.

---

## Failure Handling

Airflow Gold tasks use retries.

When a production Airflow task ultimately fails, a Telegram failure callback sends a notification containing useful task information.

The callback is designed so that a Telegram failure does not hide the original Airflow task failure.

The operational flow is:

```text
Spark task fails
      ↓
Airflow retry
      ↓
Retry exhausted
      ↓
Task marked FAILED
      ↓
Telegram notification
```

---

## Testing

The project uses pytest for automated testing.

Run the tests locally with:

```bash
uv run pytest
```

Formatting:

```bash
uv run ruff format --check .
```

Linting:

```bash
uv run ruff check .
```

The tests mock external dependencies where appropriate so unit tests do not require live Kafka, MinIO, Spark, or Telegram services.

---

## Continuous Integration

GitHub Actions runs two independent jobs.

### Quality

```text
Checkout
   ↓
Python 3.12
   ↓
uv sync --locked
   ↓
Ruff formatting
   ↓
Ruff lint
   ↓
pytest
```

### Docker

```text
Checkout
   ↓
docker compose config
   ↓
Build Airflow image
   ↓
Build Spark image
```

This ensures that both application code and infrastructure definitions are validated before changes are merged.

---

## Operational Commands

### Start everything

```bash
docker compose up -d
```

### Stop everything

```bash
docker compose down
```

### View service status

```bash
docker compose ps
```

### View Airflow scheduler logs

```bash
docker compose logs -f airflow-scheduler
```

### View Spark master logs

```bash
docker compose logs -f spark-master
```

### View Kafka logs

```bash
docker compose logs -f kafka
```

### Restart a service

```bash
docker compose restart <service>
```

### Rebuild an image

```bash
docker compose build <service>
```

---

## Data Storage

The project uses MinIO as an S3-compatible object store.

The logical data layers are:

```text
s3a://bronze/
s3a://silver/
s3a://gold/
```

Gold datasets are exposed through DuckDB views.

DuckDB reads the Parquet datasets directly, allowing analytical queries without requiring a separate analytical database.

---

## Design Decisions

### Why Kafka?

Kafka provides a durable event-streaming layer between the API producer and Spark.

This decouples ingestion from downstream processing.

### Why Spark Structured Streaming?

Spark provides distributed processing while allowing the Bronze and Silver layers to operate continuously.

### Why MinIO?

MinIO provides an S3-compatible object store suitable for local development while keeping the storage architecture similar to cloud object storage.

### Why Airflow?

Airflow is used for finite, scheduled analytical workloads where dependencies, retries, execution dates, and operational visibility are important.

### Why not Airflow for Bronze and Silver?

Bronze and Silver are continuous streaming processes.

They are not finite tasks that naturally start and finish, so they are managed as long-running Spark services rather than Airflow tasks.

### Why DuckDB?

DuckDB provides a lightweight analytical engine capable of querying the Gold Parquet datasets directly.

This avoids introducing a separate analytical database for the project.

---

## Production Considerations

The project implements several production-oriented practices:

* configuration centralized through Pydantic Settings
* secrets supplied through environment variables
* schema validation with Pydantic
* structured logging
* streaming checkpoints
* date-based Gold processing
* dynamic partition overwrite
* Airflow retries
* Telegram failure notifications
* automated tests
* linting and formatting
* Docker validation
* CI/CD

---

## Known Limitations

This project is designed as a local/cloud-learning data engineering project rather than a fully managed enterprise platform.

Potential future improvements include:

* managed Kafka
* managed object storage
* infrastructure as code
* centralized secrets management
* production monitoring and metrics
* distributed Airflow deployment
* data-quality frameworks
* schema registry
* alerting beyond task failures
* automated deployment

These are intentionally outside the current project scope.

---

## Project Outcome

This project demonstrates an end-to-end real-time data engineering architecture:

```text
API ingestion
     ↓
Kafka
     ↓
Spark Structured Streaming
     ↓
Bronze
     ↓
Silver
     ↓
Gold analytical datasets
     ↓
Airflow orchestration
     ↓
DuckDB analytics
```

It also demonstrates practical engineering concerns beyond simply processing data:

```text
Testing
CI/CD
Configuration
Secrets
Logging
Retries
Failure notifications
Idempotency
Partitioning
Docker
Orchestration
```

The project is considered complete when the pipeline can be started from a clean environment, process Citi Bike data through all layers, generate the Gold analytical datasets, expose them through DuckDB, and recover safely from expected task failures.

```
```
