from pathlib import Path

import pandas as pd

from analytics.duckdb.connection import get_connection

SQL_ROOT = Path(__file__).parent.parent / "sql"


def list_queries() -> list[str]:
    """
    Return all SQL queries relative to the SQL root.
    """
    return [str(path.relative_to(SQL_ROOT)) for path in SQL_ROOT.rglob("*.sql")]


def run_query(query: str) -> pd.DataFrame:
    """
    Execute an analytics SQL query and return the results as a DataFrame.
    """
    sql_file = SQL_ROOT / query
    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    conn = get_connection()
    sql = sql_file.read_text()
    return conn.sql(sql).df()
