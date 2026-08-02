from common.storage import bronze_checkpoint_path, bronze_path
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery


def write_bronze(df: DataFrame) -> StreamingQuery:
    return (
        df.writeStream.format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", bronze_path("station_status"))
        .option("checkpointLocation", bronze_checkpoint_path("station_status"))
        .start()
    )
