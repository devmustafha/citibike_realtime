from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType


def write_bucket(
    df: DataFrame, path: str, write_mode: str = "overwrite", partitionBy=None
) -> None:
    df.write.mode(write_mode).option("partitionOverwriteMode", "dynamic").parquet(
        path, partitionBy=partitionBy
    )


def read_bucket(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.parquet(path)


def read_stream_bucket(spark: SparkSession, schema: StructType, path: str) -> DataFrame:
    return spark.readStream.schema(schema).option("maxFilesPerTrigger", 1).parquet(path)


def write_stream_bucket(
    df: DataFrame,
    path: str,
    write_mode: str = "append",
    partitionBy=None,
    checkpointLocation: str = "",
    processingTime: str = "10 seconds",
):

    stream_writer = (
        df.writeStream.format("parquet")
        .outputMode(write_mode)
        .trigger(processingTime=processingTime)
        .option("path", path)
        .option("checkpointLocation", checkpointLocation)
    )
    if partitionBy is not None:
        stream_writer = stream_writer.partitionBy(partitionBy)

    return stream_writer.start()
