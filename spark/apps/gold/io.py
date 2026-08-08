from pyspark.sql import DataFrame, SparkSession


def write_bucket(
    df: DataFrame, path: str, write_mode: str = "overwrite", partitionBy=None
) -> None:
    df.write.mode(write_mode).option("partitionOverwriteMode", "dynamic").parquet(
        path, partitionBy=partitionBy
    )


def read_bucket(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.parquet(path)
