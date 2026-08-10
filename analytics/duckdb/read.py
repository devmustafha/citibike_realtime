from duckdb import DuckDBPyConnection, DuckDBPyRelation

from common.config import get_settings

settings = get_settings()


def _read_bucket(
    conn: DuckDBPyConnection,
    bucket: str,
    path: str = "**/*.parquet",
) -> DuckDBPyRelation:
    return conn.read_parquet(f"{bucket}/{path}", hive_partitioning=True)


def read_latest_station_status(conn: DuckDBPyConnection):
    return _read_bucket(conn, settings.latest_station_status_duckdb_path)


def read_station_hourly_metrics(conn: DuckDBPyConnection):
    return _read_bucket(conn, settings.station_hourly_metrics_duckdb_path)


def read_station_daily_metrics(conn: DuckDBPyConnection):
    return _read_bucket(conn, settings.station_daily_metrics_duckdb_path)


def read_system_metrics(conn: DuckDBPyConnection):
    return _read_bucket(conn, settings.system_metrics_duckdb_path)
