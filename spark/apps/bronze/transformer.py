from common.schemas import station_status_schema
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    current_timestamp,
    from_json,
)


def transform_station_status(df: DataFrame) -> DataFrame:
    parsed_df = df.select(
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

    return parsed_df.withColumn(
        "ingested_at",
        current_timestamp(),
    )
