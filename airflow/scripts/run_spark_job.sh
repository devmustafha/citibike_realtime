#!/usr/bin/env bash

set -euo pipefail

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SPARK_CONTAINER="citibike-spark-master"
SPARK_SUBMIT="/opt/spark/bin/spark-submit"
APP_ROOT="/opt/spark/apps"

# ---------------------------------------------------------
# Validate Input
# ---------------------------------------------------------

if [ $# -ne 1 ]; then
    echo "Usage: $0 <job_name>"
    echo ""
    echo "Available jobs:"
    echo "  bronze"
    echo "  silver"
    echo "  latest_station_status"
    echo "  station_hourly_metrics"
    echo "  station_daily_metrics"
    echo "  system_metrics"
    exit 1
fi

JOB="$1"

# ---------------------------------------------------------
# Map Job Name to Spark Application
# ---------------------------------------------------------

case "$JOB" in
    bronze)
        APP="bronze/ingest_station_status.py"
        ;;

    silver)
        APP="silver/main.py"
        ;;

    latest_station_status)
        APP="gold/latest_station_status/main.py"
        ;;

    station_hourly_metrics)
        APP="gold/station_hourly_metrics/main.py"
        ;;

    station_daily_metrics)
        APP="gold/station_daily_metrics/main.py"
        ;;

    system_metrics)
        APP="gold/system_metrics/main.py"
        ;;

    *)
        echo "Unknown Spark job: $JOB"
        exit 1
        ;;
esac

# ---------------------------------------------------------
# Submit Spark Job
# ---------------------------------------------------------

echo "======================================="
echo "Submitting Spark Job"
echo "Job       : $JOB"
echo "Script    : $APP_ROOT/$APP"
echo "Container : $SPARK_CONTAINER"
echo "======================================="

spark-submit \
    --master spark://spark-master:7077 \
    "$APP_ROOT/$APP"

echo ""
echo "======================================="
echo "Spark job completed successfully."
echo "======================================="