from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select

from adapters.postgres.database import SessionLocal
from adapters.postgres.models import RouteORM
from domain.models.route import Route
from domain.ports.route_repository_port import RouteRepositoryPort
from errors import RouteNotFoundError


class PostgresRouteRepositoryAdapter(RouteRepositoryPort):
    """SQLAlchemy-based repository implementation for routes."""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def create(self, route: Route) -> Route:
        now = datetime.now(timezone.utc).replace(microsecond=0)
        if route.id is None:
            route.id = str(uuid4())
        if route.createdAt is None:
            route.createdAt = now
        if route.updatedAt is None:
            route.updatedAt = now

        orm_route = RouteORM(
            id=route.id,
            flight_id=route.flightId,
            source_airport_code=route.sourceAirportCode,
            source_country=route.sourceCountry,
            destiny_airport_code=route.destinyAirportCode,
            destiny_country=route.destinyCountry,
            bag_cost=route.bagCost,
            planned_start_date=route.plannedStartDate,
            planned_end_date=route.plannedEndDate,
            created_at=route.createdAt,
            updated_at=route.updatedAt,
        )
        with self.session_factory() as session:
            session.add(orm_route)
            session.commit()
            session.refresh(orm_route)
            return self._to_domain(orm_route)

    def get_by_id(self, route_id: str) -> Route | None:
        with self.session_factory() as session:
            orm_route = session.get(RouteORM, route_id)
            if orm_route is None:
                return None
            return self._to_domain(orm_route)

    def get_all(self, flight_id: str | None = None) -> list[Route]:
        statement = select(RouteORM)
        if flight_id is not None:
            statement = statement.where(RouteORM.flight_id == flight_id)
        with self.session_factory() as session:
            orm_routes = session.execute(statement).scalars().all()
            return [self._to_domain(route) for route in orm_routes]

    def get_by_flight_id(self, flight_id: str) -> Route | None:
        statement = select(RouteORM).where(RouteORM.flight_id == flight_id)
        with self.session_factory() as session:
            orm_route = session.execute(statement).scalar_one_or_none()
            if orm_route is None:
                return None
            return self._to_domain(orm_route)

    def delete(self, route_id: str) -> Route:
        with self.session_factory() as session:
            orm_route = session.get(RouteORM, route_id)
            if orm_route is None:
                raise RouteNotFoundError(f"Route with id {route_id} not found")
            session.delete(orm_route)
            session.commit()
            return self._to_domain(orm_route)

    def count(self) -> int:
        with self.session_factory() as session:
            return session.query(RouteORM).count()

    def reset(self) -> None:
        with self.session_factory() as session:
            session.query(RouteORM).delete()
            session.commit()

    @staticmethod
    def _to_domain(route: RouteORM) -> Route:
        return Route(
            id=route.id,
            flightId=route.flight_id,
            sourceAirportCode=route.source_airport_code,
            sourceCountry=route.source_country,
            destinyAirportCode=route.destiny_airport_code,
            destinyCountry=route.destiny_country,
            bagCost=route.bag_cost,
            plannedStartDate=route.planned_start_date,
            plannedEndDate=route.planned_end_date,
            createdAt=route.created_at,
            updatedAt=route.updated_at,
        )
