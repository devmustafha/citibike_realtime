from pathlib import Path

import duckdb

from common.config import settings

DB_PATH = Path(__file__).parent / "analytics.duckdb"


def configure_extensions(conn):
    conn.install_extension("httpfs")
    conn.load_extension("httpfs")


def configure_s3(conn):
    conn.execute(f"SET s3_endpoint='{settings.minio_endpoint}'")
    conn.execute(f"SET s3_access_key_id='{settings.minio_access_key}'")
    conn.execute(f"SET s3_secret_access_key='{settings.minio_secret_key}'")
    conn.execute(f"SET s3_use_ssl={'true' if settings.minio_secure else 'false'}")
    conn.execute("SET s3_url_style='path'")


def get_connection() -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect(str(DB_PATH))

    # Install/load extensions
    configure_extensions(conn)

    # Configure MinIO
    configure_s3(conn)

    return conn
