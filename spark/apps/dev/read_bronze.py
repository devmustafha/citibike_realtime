from common.session import create_spark_session

from common.config import BRONZE_STATION_STATUS_PATH

spark = create_spark_session("read-bronze")

df = spark.read.parquet(BRONZE_STATION_STATUS_PATH)

df.printSchema()

df.show(truncate=False)
