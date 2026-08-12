from datetime import datetime, timedelta, timezone

import pytest

from domain.models.route import Trayecto
from domain.use_cases.create_route_use_case import CreateRouteUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError


class FakeRepository:
    def __init__(self):
        self.routes = {}

    def get_by_flight_id(self, flight_id: str):
        return self.routes.get(flight_id)

    def create(self, route: Trayecto):
        self.routes[route.flightId] = route
        return route


def test_create_route_use_case_success():
    repo = FakeRepository()
    use_case = CreateRouteUseCase(repo)

    route = Trayecto(
        flightId="FL123",
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=120.5,
        plannedStartDate=datetime.now(timezone.utc) + timedelta(days=1),
        plannedEndDate=datetime.now(timezone.utc) + timedelta(days=3),
    )

    created = use_case.execute(route)

    assert created.id is not None
    assert created.createdAt is not None
    assert repo.routes["FL123"].flightId == "FL123"


def test_create_route_use_case_rejects_duplicate_flight_id():
    repo = FakeRepository()
    repo.routes["FL123"] = Trayecto(
        id="existing-id",
        flightId="FL123",
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=50,
        plannedStartDate=datetime.now(timezone.utc) + timedelta(days=10),
        plannedEndDate=datetime.now(timezone.utc) + timedelta(days=12),
    )
    use_case = CreateRouteUseCase(repo)

    route = Trayecto(
        flightId="FL123",
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=120.5,
        plannedStartDate=datetime.now(timezone.utc) + timedelta(days=1),
        plannedEndDate=datetime.now(timezone.utc) + timedelta(days=2),
    )

    with pytest.raises(RouteAlreadyExistsError):
        use_case.execute(route)


def test_create_route_use_case_rejects_invalid_dates():
    repo = FakeRepository()
    use_case = CreateRouteUseCase(repo)

    route = Trayecto(
        flightId="FL999",
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=90,
        plannedStartDate=datetime.now(timezone.utc) + timedelta(days=2),
        plannedEndDate=datetime.now(timezone.utc) + timedelta(days=1),
    )

    with pytest.raises(InvalidRouteDatesError):
        use_case.execute(route)
