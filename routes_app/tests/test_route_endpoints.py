from uuid import uuid4

import pytest

from domain.models.route import Trayecto
from domain.use_cases.delete_route_use_case import DeleteRouteUseCase
from domain.use_cases.get_all_routes_use_case import GetAllRoutesUseCase
from domain.use_cases.get_route_use_case import GetRouteUseCase
from errors import RouteNotFoundError


class InMemoryRouteRepository:
    def __init__(self):
        self.routes = {}

    def create(self, route: Trayecto) -> Trayecto:
        self.routes[route.id] = route
        return route

    def get_by_id(self, route_id: str):
        return self.routes.get(route_id)

    def get_all(self, flight_id=None):
        all_routes = list(self.routes.values())
        if flight_id is None:
            return all_routes
        return [route for route in all_routes if route.flightId == flight_id]

    def delete(self, route_id: str):
        if route_id not in self.routes:
            raise RouteNotFoundError(f"Route with id {route_id} not found")
        return self.routes.pop(route_id)


def create_route(flight_id: str) -> Trayecto:
    return Trayecto(
        id=str(uuid4()),
        flightId=flight_id,
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=1.0,
        plannedStartDate="2099-01-01T00:00:00Z",
        plannedEndDate="2099-01-02T00:00:00Z",
    )


def test_get_all_routes_returns_all():
    repository = InMemoryRouteRepository()
    route_a = create_route("FL123")
    route_b = create_route("FL456")
    repository.create(route_a)
    repository.create(route_b)

    use_case = GetAllRoutesUseCase(repository)

    result = use_case.execute()

    assert len(result) == 2
    assert {route.flightId for route in result} == {"FL123", "FL456"}


def test_get_all_routes_filters_by_flight():
    repository = InMemoryRouteRepository()
    route_a = create_route("FL123")
    route_b = create_route("FL456")
    repository.create(route_a)
    repository.create(route_b)

    use_case = GetAllRoutesUseCase(repository)

    result = use_case.execute("FL123")

    assert len(result) == 1
    assert result[0].flightId == "FL123"


def test_get_route_returns_route():
    repository = InMemoryRouteRepository()
    route = create_route("FL123")
    repository.create(route)

    use_case = GetRouteUseCase(repository)

    result = use_case.execute(route.id)

    assert result is not None
    assert result.flightId == "FL123"


def test_get_route_returns_none_for_missing():
    repository = InMemoryRouteRepository()
    use_case = GetRouteUseCase(repository)

    result = use_case.execute(str(uuid4()))

    assert result is None


def test_delete_route_returns_deleted_route():
    repository = InMemoryRouteRepository()
    route = create_route("FL123")
    repository.create(route)

    use_case = DeleteRouteUseCase(repository)

    result = use_case.execute(route.id)

    assert result.id == route.id
    assert repository.get_by_id(route.id) is None


def test_delete_route_raises_not_found():
    repository = InMemoryRouteRepository()
    use_case = DeleteRouteUseCase(repository)

    with pytest.raises(RouteNotFoundError):
        use_case.execute(str(uuid4()))
