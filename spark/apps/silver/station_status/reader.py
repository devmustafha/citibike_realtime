from common.schemas import station_status_schema
from common.storage import bronze_path
from pyspark.sql import DataFrame, SparkSession


def read_bronze_station_status(spark: SparkSession) -> DataFrame:
    return (
        spark.readStream.schema(station_status_schema)
        .option("maxFilesPerTrigger", 1)
        .parquet(bronze_path("station_status"))
    )
