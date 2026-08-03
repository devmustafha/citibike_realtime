from common.session import create_spark_session
from common.storage import GOLD_STATION_LATEST_PATH, SILVER_STATION_STATUS_PATH
from gold.io import read_bucket, write_bucket
from transform import transform_latest_station_status


def main():
    spark = create_spark_session("latest-station-status")
    silver_df = read_bucket(spark, SILVER_STATION_STATUS_PATH)
    gold_df = transform_latest_station_status(silver_df)
    write_bucket(gold_df, GOLD_STATION_LATEST_PATH)

    spark.stop()


if __name__ == "__main__":
    main()
