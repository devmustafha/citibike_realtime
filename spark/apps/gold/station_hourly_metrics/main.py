import argparse
from datetime import date

from common.session import create_spark_session
from common.storage import GOLD_STATION_HOURLY_PATH, SILVER_STATION_STATUS_PATH
from gold.io import read_bucket, write_bucket
from transform import build_station_hourly_metrics


def main(process_date: date) -> None:
    spark = create_spark_session("gold-session")
    silver_df = read_bucket(spark, SILVER_STATION_STATUS_PATH)
    hourly_metrics = build_station_hourly_metrics(silver_df, process_date=process_date)
    write_bucket(hourly_metrics, GOLD_STATION_HOURLY_PATH, partitionBy=["hour"])

    spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--process-date",
        type=date.fromisoformat,
        required=True,
    )

    args = parser.parse_args()
    main(args.process_date)
