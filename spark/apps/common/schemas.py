from pyspark.sql.types import (
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

station_status_schema = StructType(
    [
        StructField("station_id", StringType(), False),
        StructField("num_bikes_available", IntegerType(), False),
        StructField("num_docks_available", IntegerType(), False),
        StructField("num_ebikes_available", IntegerType(), False),
        StructField("is_installed", IntegerType(), False),
        StructField("is_renting", IntegerType(), False),
        StructField("is_returning", IntegerType(), False),
        StructField("last_reported", LongType(), False),
    ]
)
