from pyspark.sql import DataFrame
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window


def transform_latest_station_status(df: DataFrame) -> DataFrame:
    window = Window.partitionBy("station_id").orderBy(col("last_reported_ts").desc())

    return (
        df.withColumn("row_num", row_number().over(window))
        .filter(col("row_num") == 1)
        .drop("row_num", "year", "month", "day")
    )
