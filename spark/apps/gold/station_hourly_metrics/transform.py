from datetime import date

from pyspark.sql import DataFrame
from pyspark.sql.functions import avg, col, hour, max, min


def build_station_hourly_metrics(df: DataFrame, process_date: date) -> DataFrame:
    return (
        df.filter(col("year") == process_date.year)
        .filter(col("month") == process_date.month)
        .filter(col("day") == process_date.day)
        .withColumn("hour", hour("last_reported_ts"))
        .groupBy("station_id", "hour")
        .agg(
            min("num_bikes_available").alias("min_bikes_available"),
            max("num_bikes_available").alias("max_bikes_available"),
            avg("num_bikes_available").alias("avg_bikes_available"),
            min("num_docks_available").alias("min_docks_available"),
            max("num_docks_available").alias("max_docks_available"),
            avg("num_docks_available").alias("avg_docks_available"),
        )
    )
