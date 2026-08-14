from __future__ import annotations

import httpx

from common.config import get_settings
from common.logging import setup_logging
from producer.models import (
    StationInformation,
    StationInformationResponse,
    StationStatusData,
    StationStatusResponse,
)

setup_logging()


class CitiBikeClient:
    """Client for retrieving Citi Bike GBFS feeds."""

    def __init__(self) -> None:
        self._client = httpx.Client(
            timeout=10,
        )

    def get_station_status(self) -> list[StationStatusData]:
        settings = get_settings()
        try:
            response = self._client.get(settings.citibike_api_url)

            response.raise_for_status()

            validated_response = StationStatusResponse.model_validate(response.json())
            stations = validated_response.data.stations
            return stations
        except httpx.HTTPError:
            raise

    def get_station_information(self) -> list[StationInformation]:
        settings = get_settings()
        try:
            response = self._client.get(settings.citibike_station_information_url)

            response.raise_for_status()

            validated_response = StationInformationResponse.model_validate(
                response.json()
            )
            station_information = validated_response.data.stations
            return station_information
        except httpx.HTTPError:
            raise

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()
