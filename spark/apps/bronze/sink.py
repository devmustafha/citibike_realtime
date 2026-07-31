from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery

from common.config import (
    BRONZE_PATH,
    CHECKPOINT_PATH,
)


def write_bronze(df: DataFrame) -> StreamingQuery:
    return (
        df.writeStream.format("parquet")
        .option("path", BRONZE_PATH)
        .option("checkpointLocation", CHECKPOINT_PATH)
        .outputMode("append")
        .start()
    )
