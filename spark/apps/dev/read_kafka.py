from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("citibike-read-kafka")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "station-status")
    .option("startingOffsets", "latest")
    .load()
)

(
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")
    .writeStream.format("console")
    .outputMode("append")
    .start()
    .awaitTermination()
)
