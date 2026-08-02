from common.session import create_spark_session
from read import read_silver_station_status
from sink import write_latest_station_status
from transform import transform_latest_station_status


def main():
    spark = create_spark_session("gold-latest-station-status")
    silver_df = read_silver_station_status(spark)
    gold_df = transform_latest_station_status(silver_df)
    write_latest_station_status(gold_df)

    spark.stop()


if __name__ == "__main__":
    main()
