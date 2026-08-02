from pyspark.sql import DataFrame

from common.config import SILVER_STATION_STATUS_CHECKPOINT, SILVER_STATION_STATUS_PATH


def write_silver_station_status(df: DataFrame):
    return (
        df.writeStream.format("parquet")
        .outputMode("append")
        .trigger(processingTime="30 seconds")
        .option("path", SILVER_STATION_STATUS_PATH)
        .option("checkpointLocation", SILVER_STATION_STATUS_CHECKPOINT)
        .partitionBy("year", "month", "day")
        .start()
    )
