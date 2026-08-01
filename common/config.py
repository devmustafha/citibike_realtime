from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    citibike_api_url: str
    kafka_bootstrap_servers: str
    poll_interval_seconds: int = 30
    kafka_station_status_topic: str = "station-status"
    bronze_station_status_path: str
    silver_station_status_path: str
    silver_station_checkpoint_path: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
