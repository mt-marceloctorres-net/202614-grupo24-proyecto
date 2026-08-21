from datetime import datetime, timedelta, timezone

import pytest

from domain.models.route import Route
from domain.use_cases.create_route_use_case import CreateRouteUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError


class FakeRepository:
    def __init__(self):
        self.routes = {}

    def get_by_flight_id(self, flight_id: str):
        return self.routes.get(flight_id)

    def create(self, route: Route):
        self.routes[route.flightId] = route
        return route


def test_create_route_use_case_success():
    repo = FakeRepository()
    use_case = CreateRouteUseCase(repo)

    route = Route(
        flightId="FL123",
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=120,
        plannedStartDate=datetime.now(timezone.utc) + timedelta(days=1),
        plannedEndDate=datetime.now(timezone.utc) + timedelta(days=3),
    )

    created = use_case.execute(route)

    assert created.id is not None
    assert created.createdAt is not None
    assert repo.routes["FL123"].flightId == "FL123"


def test_create_route_use_case_rejects_duplicate_flight_id():
    repo = FakeRepository()
    repo.routes["FL123"] = Route(
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

    route = Route(
        flightId="FL123",
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=120,
        plannedStartDate=datetime.now(timezone.utc) + timedelta(days=1),
        plannedEndDate=datetime.now(timezone.utc) + timedelta(days=2),
    )

    with pytest.raises(RouteAlreadyExistsError):
        use_case.execute(route)


def test_create_route_use_case_rejects_invalid_dates():
    repo = FakeRepository()
    use_case = CreateRouteUseCase(repo)

    route = Route(
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


def test_create_route_truncates_microseconds_in_planned_dates():
    """`plannedStartDate`/`plannedEndDate` se guardan sin microsegundos.

    Vienen directo del cliente (a diferencia de `createdAt`, que genera el
    servidor); sin truncar, `restrictions.md` queda incumplida aunque el
    pipeline no valide el formato exacto.
    """
    repo = FakeRepository()
    use_case = CreateRouteUseCase(repo)

    route = Route(
        flightId="FL2000",
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=90,
        plannedStartDate=datetime.now(timezone.utc)
        + timedelta(days=1, microseconds=123456),
        plannedEndDate=datetime.now(timezone.utc)
        + timedelta(days=2, microseconds=654321),
    )

    created = use_case.execute(route)

    assert created.plannedStartDate.microsecond == 0
    assert created.plannedEndDate.microsecond == 0
    assert created.plannedStartDate.tzinfo is None
    assert created.plannedEndDate.tzinfo is None


def test_create_route_use_case_rejects_past_dates():
    repo = FakeRepository()
    use_case = CreateRouteUseCase(repo)

    route = Route(
        flightId="FL1000",
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=90,
        plannedStartDate=datetime.now(timezone.utc) - timedelta(days=2),
        plannedEndDate=datetime.now(timezone.utc) - timedelta(days=1),
    )

    with pytest.raises(InvalidRouteDatesError):
        use_case.execute(route)
