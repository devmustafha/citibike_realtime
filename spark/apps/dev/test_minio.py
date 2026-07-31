from common.session import create_spark_session
from pyspark.sql import Row

spark = create_spark_session("test-minio")

df = spark.createDataFrame(
    [
        Row(id=1, name="Citibike"),
        Row(id=2, name="Spark"),
    ]
)

df.write.mode("overwrite").parquet("s3a://bronze/test")

spark.stop()
