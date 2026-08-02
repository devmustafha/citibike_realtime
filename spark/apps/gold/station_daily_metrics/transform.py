from datetime import date

from pyspark.sql import DataFrame
from pyspark.sql.functions import avg, col, max, min


def build_station_daily_metrics(df: DataFrame, process_date: date) -> DataFrame:
    return (
        df.filter(col("year") == process_date.year)
        .filter(col("month") == process_date.month)
        .groupBy("station_id", "day")
        .agg(
            min("num_bikes_available").alias("min_bikes_available"),
            max("num_bikes_available").alias("max_bikes_available"),
            avg("num_bikes_available").alias("avg_bikes_available"),
            min("num_docks_available").alias("min_docks_available"),
            max("num_docks_available").alias("max_docks_available"),
            avg("num_docks_available").alias("avg_docks_available"),
        )
    )
