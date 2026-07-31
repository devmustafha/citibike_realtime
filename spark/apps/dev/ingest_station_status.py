from common.schemas import station_status_schema
from common.session import create_spark_session
from pyspark.sql.functions import col, current_timestamp, from_json

from common.config import KAFKA_BOOTSTRAP, KAFKA_TOPIC


def main() -> None:
    spark = create_spark_session("bronze-station-status")

    kafka_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
        .option("subscribe", KAFKA_TOPIC)
        .load()
    )

    parsed_df = kafka_df.select(
        from_json(
            col("value").cast("string"),
            station_status_schema,
        ).alias("data"),
        col("timestamp").alias("kafka_timestamp"),
        col("topic"),
        col("partition"),
        col("offset"),
    ).select(
        "data.*",
        "kafka_timestamp",
        "topic",
        "partition",
        "offset",
    )

    bronze_df = parsed_df.withColumn(
        "ingested_at",
        current_timestamp(),
    )

    query = (
        bronze_df.writeStream.format("console")
        .outputMode("append")
        .option("truncate", "false")
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
