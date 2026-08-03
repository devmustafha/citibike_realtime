from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, day, max, month, sum, when, year
from pyspark.sql.types import DecimalType


def build_system_metrics(df: DataFrame) -> DataFrame:
    return (
        df.agg(
            sum("num_bikes_available").alias("total_bikes_available"),
            sum("num_docks_available").alias("total_docks_available"),
            sum(
                when(
                    (col("is_installed") == 1)
                    & (col("is_renting") == 1)
                    & (col("is_returning") == 1),
                    1,
                ).otherwise(0),
            ).alias("active_station_count"),
            sum(
                when(
                    (col("is_installed") == 0)
                    | (col("is_renting") == 0)
                    | (col("is_returning") == 0),
                    1,
                ).otherwise(0),
            ).alias("disabled_station_count"),
            count("station_id").alias("total_station_count"),
            max("last_reported_ts").alias("snapshot_time"),
        )
        .withColumn(
            "bike_occupancy_rate",
            (
                col("total_bikes_available")
                / (col("total_bikes_available") + col("total_docks_available"))
            ).cast(DecimalType(scale=2)),
        )
        .withColumn("year", year(col("snapshot_time")))
        .withColumn("month", month(col("snapshot_time")))
        .withColumn("day", day(col("snapshot_time")))
    )
