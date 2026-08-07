from analytics.duckdb.connection import get_connection
from common.config import get_settings


def _get_views():
    settings = get_settings()
    return {
        "latest_station_status": settings.latest_station_status_path,
        "system_metrics": settings.system_metrics_path,
        "station_hourly_metrics": settings.station_hourly_metrics_path,
        "station_daily_metrics": settings.station_daily_metrics_path,
    }


def _create_view_sql(view_name: str, bucket: str):
    return f"""
        CREATE OR REPLACE VIEW {view_name} AS 
        SELECT * FROM 
        read_parquet(
            '{bucket}/**/*.parquet'
        );
    """


def bootstrap():
    conn = get_connection()
    for view_name, bucket in _get_views().items():
        conn.execute(_create_view_sql(view_name, bucket))
    print("Successfully created all DuckDB views")


if __name__ == "__main__":
    bootstrap()
