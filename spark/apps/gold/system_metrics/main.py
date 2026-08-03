from common.session import create_spark_session
from common.storage import GOLD_STATION_LATEST_PATH, GOLD_SYSTEM_METRICS_PATH
from gold.io import read_bucket, write_bucket
from transform import build_system_metrics


def main():
    spark = create_spark_session("system_metrics_session")
    station_latest_df = read_bucket(spark, GOLD_STATION_LATEST_PATH)
    system_metrics = build_system_metrics(station_latest_df)
    write_bucket(
        system_metrics, GOLD_SYSTEM_METRICS_PATH, partitionBy=["year", "month", "day"]
    )

    spark.stop()


if __name__ == "__main__":
    main()
