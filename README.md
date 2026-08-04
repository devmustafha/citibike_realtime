# Citi Bike Realtime Lakehouse Pipeline

## Overview

This project is a real-time data engineering pipeline that ingests live
Citi Bike station status data, streams it through Apache Kafka,
processes it using Apache Spark Structured Streaming, and stores raw
data in a Bronze data lake on MinIO as Parquet files.

## High-Level Architecture

``` text
                           Citi Bike GBFS API
                                   │
                                   ▼
                         Python Producer Service
                                   │
                                   ▼
                           Apache Kafka Topic
                                   │
                                   ▼
                   Apache Spark Structured Streaming
                                   │
                                   ▼
                         MinIO Data Lake (Bronze)
                                   │
                                   ▼
                             Silver Layer
                                   │
                                   ▼
                              Gold Layer
                                   │
                                   ▼
                       DuckDB / Analytics / dbt
```

## Infrastructure

``` text
                    Docker Compose Network
┌──────────────────────────────────────────────────────────┐
│  Kafka ◄──── Kafka UI                                    │
│    │                                                     │
│    ▼                                                     │
│ Spark Master ───► Spark Worker                           │
│         │                                                │
│         ▼                                                │
│       MinIO                                              │
└──────────────────────────────────────────────────────────┘

Producer runs on the host machine during development and
publishes events to Kafka via localhost:9092.
```

## Bronze Ingestion Pipeline

``` text
Citi Bike API
      │
      ▼
Fetch station status
      │
      ▼
Serialize JSON
      │
      ▼
Publish to Kafka
      │
      ▼
Read Stream (Spark)
      │
      ▼
Parse JSON Schema
      │
      ▼
Add Metadata
      │
      ▼
Write Parquet
      │
      ▼
Bronze Bucket (MinIO)
```

## Technology Stack

-   Python
-   Apache Kafka
-   Apache Spark Structured Streaming
-   MinIO
-   Docker Compose
-   Parquet
-   JSON
-   uv

## Project Structure

``` text
citibike-realtime/
├── producer/
├── spark/
│   ├── apps/
│   │   ├── bronze/
│   │   ├── common/
│   │   ├── dev/
│   │   ├── silver/
│   │   └── gold/
│   ├── checkpoints/
│   └── warehouse/
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Roadmap

-   [x] Docker infrastructure
-   [x] Kafka integration
-   [x] Spark Structured Streaming
-   [x] Bronze ingestion
-   [x] Silver layer
-   [x] Gold layer
-   [ ] DuckDB analytics
-   [ ] dbt
-   [ ] Airflow
-   [ ] CI/CD

## License

MIT License.