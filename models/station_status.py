from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, field_validator


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

    @field_validator("last_reported", mode="before")
    @classmethod
    def parse_last_reported(cls, value: int) -> datetime:
        return unix_to_datetime(value)


class StationStatusData(BaseModel):
    stations: list[StationStatus]


class StationStatusResponse(BaseModel):
    last_updated: int
    ttl: int
    version: str
    data: StationStatusData

    @field_validator("last_updated", mode="before")
    @classmethod
    def parse_last_updated(cls, value: int) -> datetime:
        return unix_to_datetime(value)
