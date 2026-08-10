import signal
import time

from common.config import get_settings
from producer.client import CitiBikeClient
from producer.kafka import KafkaProducer

running = True


def stop_producer(signum, frame) -> None:
    global running
    running = False


def main() -> None:
    global running

    settings = get_settings()

    signal.signal(signal.SIGTERM, stop_producer)
    signal.signal(signal.SIGINT, stop_producer)

    client = CitiBikeClient()
    producer = KafkaProducer()

    try:
        while running:
            stations = client.get_station_status()

            for station in stations:
                producer.publish(
                    topic=settings.kafka_station_status_topic,
                    station=station,
                )

            producer.flush()

            # Sleep in small increments so SIGTERM is handled quickly.
            for _ in range(settings.poll_interval_seconds):
                if not running:
                    break
                time.sleep(1)

    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
