from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    citibike_api_url: str
    kafka_bootstrap_servers: str
    poll_interval_seconds: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
