from common.session import create_spark_session

from common.config import BRONZE_PATH

spark = create_spark_session("read-bronze")

df = spark.read.parquet(BRONZE_PATH)

df.printSchema()

df.show(truncate=False)
