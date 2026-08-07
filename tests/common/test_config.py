from common.config import Settings, get_settings


def test_get_settings_return_settings(monkeypatch):
    monkeypatch.setenv("CITIBIKE_API_URL", "http://test")
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    monkeypatch.setenv("BRONZE_STATION_STATUS_PATH", "bronze")
    monkeypatch.setenv("SILVER_STATION_STATUS_PATH", "silver")
    monkeypatch.setenv("SILVER_STATION_CHECKPOINT_PATH", "checkpoint")
    monkeypatch.setenv("MINIO_ENDPOINT", "localhost:9000")
    monkeypatch.setenv("MINIO_ACCESS_KEY", "test")
    monkeypatch.setenv("MINIO_SECRET_KEY", "test")

    settings = get_settings()

    assert isinstance(settings, Settings)


def test_get_settings_is_cached(monkeypatch):
    monkeypatch.setenv("CITIBIKE_API_URL", "http://test")
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    monkeypatch.setenv("BRONZE_STATION_STATUS_PATH", "bronze")
    monkeypatch.setenv("SILVER_STATION_STATUS_PATH", "silver")
    monkeypatch.setenv("SILVER_STATION_CHECKPOINT_PATH", "checkpoint")
    monkeypatch.setenv("MINIO_ENDPOINT", "localhost:9000")
    monkeypatch.setenv("MINIO_ACCESS_KEY", "test")
    monkeypatch.setenv("MINIO_SECRET_KEY", "test")

    settings_1 = get_settings()
    settings_2 = get_settings()

    assert settings_1 is settings_2
