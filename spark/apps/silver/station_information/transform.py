from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    current_date,
    current_timestamp,
    dayofmonth,
    month,
    year,
)


def transform_station_information(df: DataFrame) -> DataFrame:
    return (
        df
        # Standardize data types
        .withColumn("station_id", col("station_id").cast("string"))
        .withColumn("name", col("name").cast("string"))
        .withColumn("lat", col("lat").cast("double"))
        .withColumn("lon", col("lon").cast("double"))
        .withColumn("capacity", col("capacity").cast("int"))
        # Required fields
        .filter(col("station_id").isNotNull())
        .filter(col("lat").isNotNull())
        .filter(col("lon").isNotNull())
        # Validate coordinates
        .filter(
            (col("lat") >= -90)
            & (col("lat") <= 90)
            & (col("lon") >= -180)
            & (col("lon") <= 180)
        )
        # Capacity cannot be negative
        .filter(col("capacity").isNull() | (col("capacity") >= 0))
        # Add snapshot metadata
        .withColumn("snapshot_date", current_date())
        .withColumn("ingested_at", current_timestamp())
        # Partition columns
        .withColumn("year", year(col("snapshot_date")))
        .withColumn("month", month(col("snapshot_date")))
        .withColumn("day", dayofmonth(col("snapshot_date")))
        # One station per snapshot
        .dropDuplicates(["station_id", "snapshot_date"])
    )
