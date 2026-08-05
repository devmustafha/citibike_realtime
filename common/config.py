from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    citibike_api_url: str
    kafka_bootstrap_servers: str
    poll_interval_seconds: int = 30
    kafka_station_status_topic: str = "station-status"
    bronze_station_status_path: str
    silver_station_status_path: str
    silver_station_checkpoint_path: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_secure: bool = False
    latest_station_status_path: str = "s3a://gold/latest_station_status"
    station_hourly_metrics_path: str = "s3a://gold/station_hourly"
    station_daily_metrics_path: str = "s3a://gold/station_daily"
    system_metrics_path: str = "s3a://gold/system_metrics"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
