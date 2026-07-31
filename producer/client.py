from __future__ import annotations

import httpx

from common.config import settings
from common.logging import setup_logging
from producer.station_status import StationStatusData, StationStatusResponse

setup_logging()


class CitiBikeClient:
    """Client for retrieving Citi Bike GBFS feeds."""

    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=settings.citibike_api_url,
            timeout=10,
        )

    def get_station_status(self) -> list[StationStatusData]:
        try:
            response = self._client.get(
                settings.citibike_api_url,
                timeout=10,
            )

            response.raise_for_status()

            validated_response = StationStatusResponse.model_validate(response.json())
            stations = validated_response.data.stations
            return stations
        except httpx.HTTPError:
            raise

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()
