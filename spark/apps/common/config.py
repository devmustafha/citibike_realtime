KAFKA_TOPIC = "station-status"
KAFKA_BOOTSTRAP = "kafka:9092"

MINIO_ENDPOINT = "http://minio:9000"

BRONZE_BUCKET = "bronze"

SILVER_BUCKET = "silver"

BRONZE_STATION_STATUS_PATH = "s3a://bronze/station_status"
BRONZE_STATION_CHECKPOINT_PATH = "s3a://bronze/checkpoints/station_status"


SILVER_STATION_STATUS_PATH = f"s3a://{SILVER_BUCKET}/station_status"

SILVER_STATION_STATUS_CHECKPOINT = f"s3a://{SILVER_BUCKET}/checkpoints/station_status"
