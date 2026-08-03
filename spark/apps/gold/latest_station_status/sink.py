from common.storage import gold_path
from pyspark.sql import DataFrame


def write_latest_station_status(df: DataFrame) -> None:
    df.write.mode("overwrite").parquet(gold_path("latest_station_status"))
