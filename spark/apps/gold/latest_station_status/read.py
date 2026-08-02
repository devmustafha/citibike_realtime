from common.storage import silver_path
from pyspark.sql import DataFrame, SparkSession


def read_silver_station_status(spark: SparkSession) -> DataFrame:
    return spark.read.parquet(silver_path("station_status"))
