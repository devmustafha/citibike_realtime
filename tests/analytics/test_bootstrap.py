from unittest.mock import MagicMock, patch

from analytics.duckdb.bootstrap import _create_view_sql, _get_views, bootstrap


def test_create_view_sql():
    view_name = "latest_station_status"
    bucket = "s3a://gold/latest_station_status"
    sql = _create_view_sql(view_name, bucket)

    assert f"CREATE OR REPLACE VIEW {view_name}" in sql
    assert f"{bucket}/**/*.parquet" in sql


@patch("analytics.duckdb.bootstrap.get_connection")
def test_bootstrap_executes_all_views(mock_get_connection):
    mock_conn = MagicMock()
    mock_get_connection.return_value = mock_conn

    bootstrap()

    assert mock_conn.execute.call_count == len(_get_views())


@patch("analytics.duckdb.bootstrap.get_connection")
def test_bootstrap_creates_expected_views(mock_get_connection):
    mock_conn = MagicMock()
    mock_get_connection.return_value = mock_conn

    bootstrap()

    executed_sql = [call.args[0] for call in mock_conn.execute.call_args_list]

    for view_name in _get_views():
        assert any(f"CREATE OR REPLACE VIEW {view_name}" in sql for sql in executed_sql)
