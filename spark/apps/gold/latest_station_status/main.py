from common.session import create_spark_session
from common.station_enrichment import enrich_station_metrics
from common.storage import (
    GOLD_STATION_LATEST_PATH,
    SILVER_STATION_INFORMATION_PATH,
    SILVER_STATION_STATUS_PATH,
)
from gold.io import read_bucket, write_bucket
from transform import transform_latest_station_status


def main():
    try:
        spark = create_spark_session("latest-station-status")
        station_information_df = read_bucket(spark, SILVER_STATION_INFORMATION_PATH)
        silver_df = read_bucket(spark, SILVER_STATION_STATUS_PATH)
        enriched_df = enrich_station_metrics(silver_df, station_information_df)
        gold_df = transform_latest_station_status(enriched_df)
        write_bucket(gold_df, GOLD_STATION_LATEST_PATH)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
