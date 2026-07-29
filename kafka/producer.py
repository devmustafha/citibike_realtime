from __future__ import annotations

import logging

from confluent_kafka import Producer

from common.config import settings
from models.station_status import StationStatus

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self):
        self._producer = Producer(
            {"bootstrap.servers": settings.kafka_bootstrap_servers}
        )

    def send_station(self, station: StationStatus):
        self._producer.produce(
            topic=settings.kafka_station_status_topic,
            key=station.station_id,
            value=station.model_dump_json(),
            callback=self._delivery_report,
        )

        # Trigger delivery callbacks without blocking
        self._producer.poll(0)

    def flush(self) -> None:
        self._producer.flush()

    @staticmethod
    def _delivery_report(err, msg) -> None:
        if err is not None:
            logger.error("Failed to deliver message: %s", err)
            return

        logger.info(
            "Delivered station %s to %s [%s] @ offset %s",
            msg.key().decode(),
            msg.topic(),
            msg.partition(),
            msg.offset(),
        )
