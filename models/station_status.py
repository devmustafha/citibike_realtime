from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel


def unix_to_datetime(value: int) -> datetime:
    return datetime.fromtimestamp(value, tz=UTC)


class StationStatus(BaseModel):
    station_id: str
    num_bikes_available: int
    num_docks_available: int
    num_ebikes_available: int
    is_installed: int
    is_renting: int
    is_returning: int
    last_reported: int


class StationStatusData(BaseModel):
    stations: list[StationStatus]


class StationStatusResponse(BaseModel):
    last_updated: int
    ttl: int
    version: str
    data: StationStatusData
