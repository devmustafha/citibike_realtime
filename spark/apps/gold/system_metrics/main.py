from common.session import create_spark_session
from common.station_enrichment import enrich_station_metrics
from common.storage import (
    GOLD_STATION_LATEST_PATH,
    GOLD_SYSTEM_METRICS_PATH,
    SILVER_STATION_INFORMATION_PATH,
)
from gold.io import read_bucket, write_bucket
from transform import build_system_metrics


def main():
    spark = create_spark_session("system_metrics_session")
    station_latest_df = read_bucket(spark, GOLD_STATION_LATEST_PATH)
    station_information_df = read_bucket(spark, SILVER_STATION_INFORMATION_PATH)
    enriched_df = enrich_station_metrics(station_latest_df, station_information_df)
    system_metrics = build_system_metrics(enriched_df)
    write_bucket(
        system_metrics, GOLD_SYSTEM_METRICS_PATH, partitionBy=["year", "month", "day"]
    )

    spark.stop()


if __name__ == "__main__":
    main()
