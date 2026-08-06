from client import CitiBikeClient
from kafka import KafkaProducer

from common.config import get_settings

settings = get_settings()


def main() -> None:
    client = CitiBikeClient()
    producer = KafkaProducer()

    stations = client.get_station_status()

    for station in stations:
        producer.publish(
            topic=settings.kafka_station_status_topic,
            station=station,
        )

    producer.flush()


if __name__ == "__main__":
    main()
