from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from domain.models.route import Route


def _valid_route_data() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "flightId": "FL-100",
        "sourceAirportCode": "BOG",
        "sourceCountry": "Colombia",
        "destinyAirportCode": "MEX",
        "destinyCountry": "Mexico",
        "bagCost": 120,
        "plannedStartDate": now + timedelta(days=2),
        "plannedEndDate": now + timedelta(days=3),
    }


def test_create_route_with_valid_data():
    route = Route(**_valid_route_data())

    assert route.id is None
    assert route.flightId == "FL-100"
    assert route.sourceAirportCode == "BOG"
    assert route.destinyAirportCode == "MEX"
    assert route.bagCost == 120


def test_create_route_with_id_and_timestamps():
    now = datetime.now(timezone.utc)
    route = Route(
        **_valid_route_data(),
        id="route-1",
        createdAt=now,
        updatedAt=now,
    )

    assert route.id == "route-1"
    assert route.createdAt == now
    assert route.updatedAt == now


def test_create_route_rejects_empty_flight_id():
    with pytest.raises(ValidationError) as exc_info:
        Route(**{**_valid_route_data(), "flightId": ""})

    assert "flightId" in str(exc_info.value)


def test_create_route_rejects_non_positive_bag_cost():
    with pytest.raises(ValidationError) as exc_info:
        Route(**{**_valid_route_data(), "bagCost": 0})

    assert "bagCost" in str(exc_info.value)


def test_create_route_rejects_extra_fields():
    with pytest.raises(ValidationError) as exc_info:
        Route(**{**_valid_route_data(), "unexpected": "value"})

    assert "extra_forbidden" in str(exc_info.value)


def test_route_model_dict_conversion():
    route = Route(**_valid_route_data(), id="route-2")

    route_dict = route.model_dump()

    assert route_dict["id"] == "route-2"
    assert route_dict["flightId"] == "FL-100"
    assert route_dict["sourceCountry"] == "Colombia"
    assert route_dict["destinyCountry"] == "Mexico"
