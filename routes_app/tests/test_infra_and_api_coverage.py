from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from adapters.postgres import (
    BaseORM,
    PostgresRouteRepositoryAdapter,
    RouteORM,
    SessionLocal,
)
from assembly import (
    build_count_routes_use_case,
    build_create_route_use_case,
    build_delete_route_use_case,
    build_get_all_routes_use_case,
    build_get_route_use_case,
    build_reset_routes_use_case,
    build_route_repository,
    repository,
)
from config import Settings
from domain.models.route import Route
from domain.use_cases.count_routes_use_case import CountRoutesUseCase
from domain.use_cases.create_route_use_case import CreateRouteUseCase
from domain.use_cases.delete_route_use_case import DeleteRouteUseCase
from domain.use_cases.get_all_routes_use_case import GetAllRoutesUseCase
from domain.use_cases.get_route_use_case import GetRouteUseCase
from domain.use_cases.reset_routes_use_case import ResetRoutesUseCase
from entrypoints.api.main import app
from entrypoints.api.routers.route_router import (
    RouteCreate,
    create_route,
    delete_route,
    get_route,
    get_routes,
    get_routes_count,
    health_check,
    reset_routes,
)
from entrypoints.api.routers.route_router import router as route_router
from errors import InvalidRouteDatesError, RouteAlreadyExistsError, RouteNotFoundError


class DummyUseCase:
    def __init__(self, value=None, error=None):
        self.value = value
        self.error = error

    def execute(self, *args, **kwargs):
        if self.error is not None:
            raise self.error
        return self.value


def _build_route(flight_id: str = "FL123") -> Route:
    now = datetime.now(timezone.utc)
    return Route(
        id=str(uuid4()),
        flightId=flight_id,
        sourceAirportCode="BOG",
        sourceCountry="Colombia",
        destinyAirportCode="MEX",
        destinyCountry="Mexico",
        bagCost=100,
        plannedStartDate=now + timedelta(days=1),
        plannedEndDate=now + timedelta(days=2),
        createdAt=now,
        updatedAt=now,
    )


def _build_route_create(route: Route) -> RouteCreate:
    return RouteCreate(**route.model_dump(exclude={"id", "createdAt", "updatedAt"}))


def _build_orm(route_id: str = "r1", flight_id: str = "FL123") -> RouteORM:
    now = datetime.now(timezone.utc)
    return RouteORM(
        id=route_id,
        flight_id=flight_id,
        source_airport_code="BOG",
        source_country="Colombia",
        destiny_airport_code="MEX",
        destiny_country="Mexico",
        bag_cost=10.0,
        planned_start_date=now,
        planned_end_date=now + timedelta(days=1),
        created_at=now,
        updated_at=now,
    )


def test_settings_use_env_values(monkeypatch):
    Settings.database_url.cache_clear()
    Settings.app_name.cache_clear()
    Settings.log_level.cache_clear()

    monkeypatch.setenv("DB_HOST", "db")
    monkeypatch.setenv("DB_PORT", "5433")
    monkeypatch.setenv("DB_NAME", "routes")
    monkeypatch.setenv("DB_USER", "user")
    monkeypatch.setenv("DB_PASSWORD", "secret")
    monkeypatch.setenv("APP_NAME", "Routes API")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    assert Settings.database_url() == "postgresql+psycopg2://user:secret@db:5433/routes"
    assert Settings.app_name() == "Routes API"
    assert Settings.log_level() == "DEBUG"


def test_postgres_public_exports_are_available():
    assert BaseORM is not None
    assert RouteORM is not None
    assert SessionLocal is not None
    assert PostgresRouteRepositoryAdapter is not None


def test_assembly_builders_return_expected_types():
    assert build_route_repository() is repository
    assert isinstance(build_create_route_use_case(), CreateRouteUseCase)
    assert isinstance(build_get_all_routes_use_case(), GetAllRoutesUseCase)
    assert isinstance(build_get_route_use_case(), GetRouteUseCase)
    assert isinstance(build_delete_route_use_case(), DeleteRouteUseCase)
    assert isinstance(build_count_routes_use_case(), CountRoutesUseCase)
    assert isinstance(build_reset_routes_use_case(), ResetRoutesUseCase)


def test_main_includes_routes_router():
    paths = {getattr(route, "path", None) for route in app.routes}
    if "/routes/ping" in paths:
        return

    included_routers = []
    for route in app.routes:
        original_router = getattr(route, "original_router", None)
        if original_router is not None:
            included_routers.append(original_router)

        include_context = getattr(route, "include_context", None)
        included_router = getattr(include_context, "included_router", None)
        if included_router is not None:
            included_routers.append(included_router)

    assert any(candidate is route_router for candidate in included_routers)


def test_router_functions_happy_paths():
    route = _build_route("FL777")

    assert health_check() == "pong"
    assert get_routes_count(use_case=DummyUseCase(3)) == {"count": 3}
    assert reset_routes(use_case=DummyUseCase({"msg": "ok"})) == {"msg": "ok"}
    assert len(get_routes("FL777", use_case=DummyUseCase([route]))) == 1
    assert get_route(uuid4(), use_case=DummyUseCase(route)).id == route.id
    deleted = delete_route(uuid4(), use_case=DummyUseCase(route))
    assert deleted.msg == "el trayecto fue eliminado"


def test_router_functions_raise_http_exceptions_on_errors():
    with pytest.raises(HTTPException) as not_found_err:
        get_route(uuid4(), use_case=DummyUseCase(None))
    assert not_found_err.value.status_code == 404

    with pytest.raises(HTTPException) as delete_err:
        delete_route(
            uuid4(),
            use_case=DummyUseCase(error=RouteNotFoundError("route missing")),
        )
    assert delete_err.value.status_code == 404

    route = _build_route("FLC")
    created = create_route(_build_route_create(route), use_case=DummyUseCase(route))
    assert created.id == route.id
    assert created.createdAt == route.createdAt


def test_create_route_maps_known_business_errors_to_412():
    route_in = _build_route_create(_build_route("FL412"))

    with pytest.raises(HTTPException) as duplicate_err:
        create_route(
            route_in,
            use_case=DummyUseCase(error=RouteAlreadyExistsError("duplicate")),
        )
    assert duplicate_err.value.status_code == 412

    with pytest.raises(HTTPException) as invalid_dates_err:
        create_route(
            route_in,
            use_case=DummyUseCase(error=InvalidRouteDatesError("invalid dates")),
        )
    assert invalid_dates_err.value.status_code == 412


def test_repository_create_assigns_defaults_and_persists():
    session = MagicMock()
    session.__enter__.return_value = session
    adapter = PostgresRouteRepositoryAdapter(session_factory=lambda: session)
    route = _build_route("FL201")
    route.id = None
    route.createdAt = None
    route.updatedAt = None

    created = adapter.create(route)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert created.id is not None
    assert created.flightId == "FL201"


def test_repository_get_by_id_and_delete_flows():
    session = MagicMock()
    session.__enter__.return_value = session
    adapter = PostgresRouteRepositoryAdapter(session_factory=lambda: session)

    orm_route = _build_orm(route_id="r-id", flight_id="FLL")
    session.get.return_value = orm_route

    found = adapter.get_by_id("r-id")
    deleted = adapter.delete("r-id")

    assert found is not None
    assert found.id == "r-id"
    assert deleted.flightId == "FLL"


def test_repository_get_by_id_and_get_by_flight_id_return_none_when_missing():
    session = MagicMock()
    session.__enter__.return_value = session
    adapter = PostgresRouteRepositoryAdapter(session_factory=lambda: session)

    session.get.return_value = None
    session.execute.return_value.scalar_one_or_none.return_value = None

    assert adapter.get_by_id("missing") is None
    assert adapter.get_by_flight_id("missing") is None


def test_repository_get_all_get_by_flight_count_and_reset():
    session = MagicMock()
    session.__enter__.return_value = session
    adapter = PostgresRouteRepositoryAdapter(session_factory=lambda: session)

    orm_a = _build_orm(route_id="a", flight_id="FA")
    orm_b = _build_orm(route_id="b", flight_id="FB")

    session.execute.return_value.scalars.return_value.all.return_value = [orm_a, orm_b]
    session.query.return_value.count.return_value = 2

    all_routes = adapter.get_all()
    filtered_routes = adapter.get_all("FA")

    session.execute.return_value.scalar_one_or_none.return_value = orm_a
    by_flight = adapter.get_by_flight_id("FA")

    count = adapter.count()
    adapter.reset()

    assert len(all_routes) == 2
    assert len(filtered_routes) == 2
    assert by_flight is not None
    assert by_flight.id == "a"
    assert count == 2
    session.query.return_value.delete.assert_called_once()


def test_repository_delete_raises_when_route_not_found():
    session = MagicMock()
    session.__enter__.return_value = session
    adapter = PostgresRouteRepositoryAdapter(session_factory=lambda: session)
    session.get.return_value = None

    with pytest.raises(RouteNotFoundError):
        adapter.delete("missing")
