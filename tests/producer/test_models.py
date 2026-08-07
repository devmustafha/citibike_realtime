import pytest
from pydantic import ValidationError

from producer.models import StationStatus, StationStatusData, StationStatusResponse

valid_station_status = StationStatus(
    station_id="123",
    num_bikes_available=10,
    num_docks_available=5,
    num_ebikes_available=3,
    is_installed=1,
    is_renting=1,
    is_returning=1,
    last_reported=1720000000,
)

valid_station_status_data = StationStatusData(stations=[valid_station_status])

valid_station_status_response = StationStatusResponse(
    last_updated=2,
    ttl=30,
    version="3.0",
    data=valid_station_status_data,
)


def test_station_status_valid():
    assert valid_station_status.station_id == "123"
    assert valid_station_status.num_bikes_available == 10
    assert valid_station_status.is_installed == 1


def test_station_status_requires_required_fields():
    with pytest.raises(ValidationError):
        StationStatus(
            station_id="123",
            num_bikes_available=10,
            num_docks_available=5,
            num_ebikes_available=3,
            is_installed=1,
            is_renting=1,
            # is_returning missing
            last_reported=1720000000,
        )


def test_station_status_rejects_invalid_type():
    with pytest.raises(ValidationError):
        StationStatus(
            station_id="123",
            num_bikes_available="not-a-number",
            num_docks_available=5,
            num_ebikes_available=3,
            is_installed=1,
            is_renting=1,
            is_returning=1,
            last_reported=1720000000,
        )


def test_station_status_data_accepts_stations():
    assert len(valid_station_status_data.stations) == 1
    assert valid_station_status_data.stations[0].station_id == "123"


def test_station_status_response():
    response = valid_station_status_response

    assert response.version == "3.0"
    assert response.ttl == 30
    assert len(response.data.stations) == 1
