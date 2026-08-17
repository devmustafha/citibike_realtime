from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_date


def enrich_station_metrics(
    metrics_df: DataFrame,
    station_information_df: DataFrame,
) -> DataFrame:

    station_info = station_information_df.select(
        "station_id",
        "snapshot_date",
        "name",
        "lat",
        "lon",
        "capacity",
    )

    return (
        metrics_df.alias("m")
        .join(
            station_info.alias("si"),
            (
                (col("m.station_id") == col("si.station_id"))
                & (to_date(col("m.last_reported_ts")) == col("si.snapshot_date"))
            ),
            "left",
        )
        .select(
            col("m.*"), col("si.name"), col("si.lat"), col("si.lon"), col("si.capacity")
        )
    )
