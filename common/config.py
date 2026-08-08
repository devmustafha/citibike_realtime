from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    citibike_api_url: str = "https://gbfs.lyft.com/gbfs/2.3/bkn/fr/station_status.json"
    kafka_bootstrap_servers: str
    poll_interval_seconds: int = 30
    kafka_station_status_topic: str = "station-status"
    bronze_station_status_path: str = "s3a://bronze/station_status"
    silver_station_status_path: str = "s3a://silver/station_status"
    silver_station_checkpoint_path: str = "s3a://silver/station_status/checkpoint"

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_secure: bool = False

    latest_station_status_path: str = "s3a://gold/latest_station_status"

    station_hourly_metrics_path: str = "s3a://gold/station_hourly"

    station_daily_metrics_path: str = "s3a://gold/station_daily"

    system_metrics_path: str = "s3a://gold/system_metrics"

    telegram_bot_token: str
    telegram_chat_id: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
