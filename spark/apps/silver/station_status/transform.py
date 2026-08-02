from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    dayofmonth,
    from_unixtime,
    month,
    to_timestamp,
    year,
)


def transform_station_status(df: DataFrame) -> DataFrame:
    """
    Clean and standardize Bronze station status data.
    """

    return (
        df
        # Remove invalid rows
        .filter(col("station_id").isNotNull())
        .filter(col("last_reported").isNotNull())
        # Convert Unix timestamp
        .withColumn(
            "last_reported_ts", to_timestamp(from_unixtime(col("last_reported")))
        )
        # Partition columns
        .withColumn("year", year(col("last_reported_ts")))
        .withColumn("month", month(col("last_reported_ts")))
        .withColumn("day", dayofmonth(col("last_reported_ts")))
    )
