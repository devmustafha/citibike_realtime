from common.io import read_bucket, write_bucket
from common.session import create_spark_session
from common.storage import (
    BRONZE_STATION_INFORMATION_PATH,
    SILVER_STATION_INFORMATION_PATH,
)
from silver.station_information.transform import transform_station_information


def write_silver_station_information():
    try:
        spark = create_spark_session("station-information-silver")
        bronze_df = read_bucket(spark, BRONZE_STATION_INFORMATION_PATH)
        silver_df = transform_station_information(bronze_df)
        write_bucket(
            silver_df,
            SILVER_STATION_INFORMATION_PATH,
            partitionBy=["year", "month", "day"],
        )
    finally:
        spark.stop()


if __name__ == "__main__":
    write_silver_station_information()
