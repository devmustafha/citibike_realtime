from datetime import date

from pyspark.sql import DataFrame
from pyspark.sql.functions import avg, col, count, max, min
from pyspark.sql.types import DecimalType

from common.config import EXPECTED_OBSERVATIONS_PER_DAY


def build_station_daily_metrics(df: DataFrame, process_date: date) -> DataFrame:
    return (
        df.filter(col("year") == process_date.year)
        .filter(col("month") == process_date.month)
        .filter(col("day") == process_date.day)
        .groupBy("station_id", "year", "month", "day", "name", "capacity")
        .agg(
            min("num_bikes_available").alias("min_bikes_available"),
            max("num_bikes_available").alias("max_bikes_available"),
            avg("num_bikes_available").alias("avg_bikes_available"),
            min("num_docks_available").alias("min_docks_available"),
            max("num_docks_available").alias("max_docks_available"),
            avg("num_docks_available").alias("avg_docks_available"),
            count("*").alias("observation_count"),
        )
        .withColumn(
            "avg_bike_occupancy_rate",
            (
                col("avg_bikes_available")
                / (col("avg_bikes_available") + col("avg_docks_available"))
            ).cast(DecimalType(scale=2)),
        )
        .withColumn(
            "is_complete_day",
            (col("observation_count") / EXPECTED_OBSERVATIONS_PER_DAY) > 0.9,
        )
    )
