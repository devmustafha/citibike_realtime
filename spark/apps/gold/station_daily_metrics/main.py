from datetime import date

from common.session import create_spark_session
from common.storage import GOLD_STATION_DAILY_PATH, SILVER_STATION_STATUS_PATH
from gold.io import read_bucket, write_bucket
from transform import build_station_daily_metrics

working_date = date.today()


def main() -> None:
    spark = create_spark_session("gold-session")
    silver_df = read_bucket(spark, SILVER_STATION_STATUS_PATH)
    daily_metrics = build_station_daily_metrics(silver_df, process_date=working_date)
    write_bucket(daily_metrics, GOLD_STATION_DAILY_PATH, partitionBy=["day"])

    spark.stop()


if __name__ == "__main__":
    main()
