from __future__ import annotations

import logging

from producer.kafka import KafkaProducer

from .client import CitiBikeClient

logger = logging.getLogger(__name__)


class ProducerService:
    def __init__(self) -> None:
        self._client = CitiBikeClient()
        self._producer = KafkaProducer()

    def run(self) -> None:
        logger.info("Fetching station status")

        response = self._client.fetch_station_status()

        logger.info("Retrieved %d stations", len(response.data.stations))

        for station in response.data.stations:
            self._producer.send_station(station)

        self._producer.flush()

        logger.info("Published %d stations", len(response.data.stations))

    def close(self) -> None:
        self._client.close()
