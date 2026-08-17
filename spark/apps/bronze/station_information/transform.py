from pyspark.sql import DataFrame
from pyspark.sql.functions import current_timestamp


def transform_station_information_api_data(df: DataFrame) -> DataFrame:
    parsed_df = df.select("name", "capacity", "station_id", "lat", "lon")

    return parsed_df.withColumn("ingested_at", current_timestamp())
