from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery

from common.config import BRONZE_STATION_CHECKPOINT_PATH, BRONZE_STATION_STATUS_PATH


def write_bronze(df: DataFrame) -> StreamingQuery:
    return (
        df.writeStream.format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", BRONZE_STATION_STATUS_PATH)
        .option("checkpointLocation", BRONZE_STATION_CHECKPOINT_PATH)
        .start()
    )
