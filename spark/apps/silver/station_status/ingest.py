from common.session import create_spark_session
from silver.station_status.reader import (
    read_bronze_station_status,
)
from silver.station_status.sink import write_silver_station_status
from silver.station_status.transform import transform_station_status


def main():
    spark = create_spark_session("silver-test")

    bronze_df = read_bronze_station_status(spark)

    silver_df = transform_station_status(bronze_df)

    query = write_silver_station_status(silver_df)

    query.awaitTermination()


if __name__ == "__main__":
    main()
