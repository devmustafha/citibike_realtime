from pyspark.sql import DataFrame, SparkSession


def write_gold(
    df: DataFrame, path: str, write_mode: str = "overwrite", partitionBy=None
) -> None:
    df.write.mode(write_mode).parquet(path, partitionBy=partitionBy)


def read_silver(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.parquet(path)
