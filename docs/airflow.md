# Airflow Operations

## DAGs

The project currently uses Airflow to orchestrate finite Gold workloads.

### latest_station_status

Runs every 15 minutes.

Generates the latest station snapshot and system metrics.

### station_hourly_metrics

Runs every 15 minutes.

Processes the current processing date and generates station-level hourly metrics.

### station_daily_metrics

Runs every 15 minutes.

Processes the current processing date and generates station-level daily metrics.

## Why Bronze and Silver are not DAGs

Bronze and Silver are long-running Spark Structured Streaming applications.

They are intentionally managed as continuous Spark processes rather than Airflow tasks.

Airflow is responsible for finite analytical workloads.

## Failure handling

Gold tasks have retries configured.

After retries are exhausted, the failure callback sends a Telegram notification.

## Re-running a Gold task

Gold jobs receive an explicit processing date.

A task can therefore be rerun for a specific date without depending on the current system date.

Gold writes use dynamic partition overwrite, making retries safe.

## Checking task logs

Open Airflow and navigate to:

DAG → Task → Logs

For Spark-level errors, inspect the Spark master/worker logs as well.

## Restarting Airflow

```bash
docker compose restart airflow-scheduler airflow-webserver