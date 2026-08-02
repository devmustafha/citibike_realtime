from common.session import create_spark_session
from common.storage import bronze_path

spark = create_spark_session("read-bronze")

df = spark.read.parquet(bronze_path("station_status"))

df.printSchema()

df.show(truncate=False)
