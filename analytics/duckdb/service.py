from pathlib import Path

from analytics.duckdb.connection import get_connection
from duckdb import DuckDBPyRelation

SQL_ROOT = Path(__file__).parent.parent / "sql"


def run_query(query: str) -> DuckDBPyRelation:
    sql_file = SQL_ROOT / query
    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    conn = get_connection()
    return conn.sql(sql_file.read_text())
