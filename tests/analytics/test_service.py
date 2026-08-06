import pandas as pd
import pytest

from analytics.duckdb.service import list_queries, run_query


def test_list_queries_returns_sql_files():
    queries = list_queries()

    assert queries
    assert all(query.endswith(".sql") for query in queries)


def test_all_queries_execute():
    for query in list_queries():
        df = run_query(query)

        assert isinstance(df, pd.DataFrame)


def test_missing_query():
    with pytest.raises(FileNotFoundError):
        run_query("system/does_not_exist.sql")
