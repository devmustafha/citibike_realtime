from datetime import date

from common.session import create_spark_session
from common.storage import GOLD_STATION_HOURLY_PATH, SILVER_STATION_STATUS_PATH
from gold.io import read_silver, write_gold
from transform import build_station_hourly_metrics


def main() -> None:
    spark = create_spark_session("gold-session")
    silver_df = read_silver(spark, SILVER_STATION_STATUS_PATH)
    hourly_metrics = build_station_hourly_metrics(silver_df, process_date=date.today())
    write_gold(hourly_metrics, GOLD_STATION_HOURLY_PATH, partitionBy=["hour"])

    spark.stop()


if __name__ == "__main__":
    main()
