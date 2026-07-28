from __future__ import annotations

import httpx

from common.config import settings


class CitiBikeClient:
    """Client for retrieving Citi Bike GBFS feeds."""

    def __init__(self) -> None:
        self._client = httpx.Client(timeout=10.0)

    def fetch_station_status(self) -> dict:
        """Fetch the latest station status feed."""
        response = self._client.get(settings.citibike_api_url)

        response.raise_for_status()

        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()
