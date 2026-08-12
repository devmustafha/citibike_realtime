from bronze.station_status.transform import transform_station_status
from common.io import write_stream_bucket
from common.kafka import read_kafka_stream
from common.session import create_spark_session
from common.storage import (
    BRONZE_STATION_STATUS_CHECKPOINT_PATH,
    BRONZE_STATION_STATUS_PATH,
)

from common.config import KAFKA_BOOTSTRAP, KAFKA_TOPIC


def main() -> None:
    spark = create_spark_session("bronze-station-status")
    kafka_df = read_kafka_stream(spark, KAFKA_BOOTSTRAP, KAFKA_TOPIC)

    bronze_df = transform_station_status(kafka_df)

    query = write_stream_bucket(
        bronze_df,
        path=BRONZE_STATION_STATUS_PATH,
        checkpointLocation=BRONZE_STATION_STATUS_CHECKPOINT_PATH,
        processingTime="30 seconds",
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
