from common.config import (
    BRONZE_BUCKET,
    GOLD_BUCKET,
    SILVER_BUCKET,
)


def bronze_path(dataset: str) -> str:
    return f"s3a://{BRONZE_BUCKET}/{dataset}"


def silver_path(dataset: str) -> str:
    return f"s3a://{SILVER_BUCKET}/{dataset}"


def gold_path(dataset: str) -> str:
    return f"s3a://{GOLD_BUCKET}/{dataset}"


def bronze_checkpoint_path(dataset: str) -> str:
    return f"s3a://{BRONZE_BUCKET}/checkpoints/{dataset}"


def silver_checkpoint_path(dataset: str) -> str:
    return f"s3a://{SILVER_BUCKET}/checkpoints/{dataset}"


def gold_checkpoint_path(dataset: str) -> str:
    return f"s3a://{GOLD_BUCKET}/checkpoints/{dataset}"


SILVER_STATION_STATUS_PATH = f"s3a://{SILVER_BUCKET}/station_status"

GOLD_STATION_LATEST_PATH = f"s3a://{GOLD_BUCKET}/station_latest"
GOLD_STATION_HOURLY_PATH = f"s3a://{GOLD_BUCKET}/station_hourly"
GOLD_STATION_DAILY_PATH = f"s3a://{GOLD_BUCKET}/station_daily"
