from common.io import read_stream_bucket, write_stream_bucket
from common.schemas import station_status_schema
from common.session import create_spark_session
from common.storage import (
    BRONZE_STATION_STATUS_PATH,
    SILVER_STATION_STATUS_CHECKPOINT_PATH,
    SILVER_STATION_STATUS_PATH,
)
from silver.station_status.transform import transform_station_status


def main():
    spark = create_spark_session("silver-test")

    bronze_df = read_stream_bucket(
        spark, station_status_schema, BRONZE_STATION_STATUS_PATH
    )
    silver_df = transform_station_status(bronze_df)
    query = write_stream_bucket(
        silver_df,
        path=SILVER_STATION_STATUS_PATH,
        partitionBy=["year", "month", "day"],
        checkpointLocation=SILVER_STATION_STATUS_CHECKPOINT_PATH,
        processingTime="30 seconds",
    )
    query.awaitTermination()


if __name__ == "__main__":
    main()
