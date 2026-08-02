from common.storage import silver_checkpoint_path, silver_path
from pyspark.sql import DataFrame


def write_silver_station_status(df: DataFrame):
    return (
        df.writeStream.format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", silver_path("station_status"))
        .option("checkpointLocation", silver_checkpoint_path("station_status"))
        .partitionBy("year", "month", "day")
        .start()
    )
