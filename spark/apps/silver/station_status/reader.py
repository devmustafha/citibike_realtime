from common.schemas import station_status_schema
from pyspark.sql import DataFrame, SparkSession

from common.config import BRONZE_STATION_STATUS_PATH


def read_bronze_station_status(spark: SparkSession) -> DataFrame:
    return (
        spark.readStream.schema(station_status_schema)
        .option("maxFilesPerTrigger", 1)
        .parquet(BRONZE_STATION_STATUS_PATH)
    )
