from bronze.transformer import transform_station_status
from common.kafka import read_kafka_stream
from common.session import create_spark_session
from sink import write_bronze

from common.config import KAFKA_BOOTSTRAP, KAFKA_TOPIC


def main() -> None:
    spark = create_spark_session("bronze-station-status")

    kafka_df = read_kafka_stream(spark, KAFKA_BOOTSTRAP, KAFKA_TOPIC)

    bronze_df = transform_station_status(kafka_df)

    query = write_bronze(bronze_df)

    query.awaitTermination()


if __name__ == "__main__":
    main()
