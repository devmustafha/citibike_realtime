import argparse
from datetime import date

from common.session import create_spark_session
from common.station_enrichment import enrich_station_metrics
from common.storage import (
    GOLD_STATION_DAILY_PATH,
    SILVER_STATION_INFORMATION_PATH,
    SILVER_STATION_STATUS_PATH,
)
from gold.io import read_bucket, write_bucket
from transform import build_station_daily_metrics


def main(process_date: date) -> None:
    spark = create_spark_session("gold-session")
    silver_df = read_bucket(spark, SILVER_STATION_STATUS_PATH)
    station_information_df = read_bucket(spark, SILVER_STATION_INFORMATION_PATH)
    enriched_df = enrich_station_metrics(silver_df, station_information_df)
    daily_metrics = build_station_daily_metrics(enriched_df, process_date=process_date)
    write_bucket(
        daily_metrics, GOLD_STATION_DAILY_PATH, partitionBy=["year", "month", "day"]
    )

    spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--process-date", type=date.fromisoformat, required=True)
    args = parser.parse_args()
    main(args.process_date)
