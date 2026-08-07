from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from analytics.duckdb.service import list_queries, run_query


def test_list_queries_returns_sql_files():
    queries = list_queries()

    assert queries
    assert all(query.endswith(".sql") for query in queries)


def test_missing_query():
    with pytest.raises(FileNotFoundError):
        run_query("system/does_not_exist.sql")


@patch("analytics.duckdb.service.get_connection")
def test_run_query_returns_dataframe(mock_get_connection):
    expected = pd.DataFrame({"a": [1]})

    mock_relation = MagicMock()
    mock_relation.df.return_value = expected

    mock_conn = MagicMock()
    mock_conn.sql.return_value = mock_relation

    mock_get_connection.return_value = mock_conn

    df = run_query("systems/health.sql")

    assert df.equals(expected)

    mock_conn.sql.assert_called_once()
