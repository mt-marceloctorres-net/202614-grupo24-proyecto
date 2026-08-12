from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from adapters.postgres.database import SessionLocal
from adapters.postgres.models import RouteORM
from domain.models.route import Trayecto
from domain.ports.route_repository_port import RouteRepositoryPort
from errors import RouteNotFoundError


class PostgresRouteRepositoryAdapter(RouteRepositoryPort):
    """SQLAlchemy-based repository implementation for routes."""

    def __init__(self, session: Optional[Session] = None):
        self.session = session or SessionLocal()

    def create(self, route: Trayecto) -> Trayecto:
        now = datetime.now(timezone.utc)
        if route.id is None:
            route.id = str(now.timestamp()).replace(".", "")
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
        self.session.add(orm_route)
        self.session.commit()
        self.session.refresh(orm_route)
        return self._to_domain(orm_route)

    def get_by_id(self, route_id: str) -> Optional[Trayecto]:
        orm_route = self.session.get(RouteORM, route_id)
        if orm_route is None:
            return None
        return self._to_domain(orm_route)

    def get_all(self, flight_id: Optional[str] = None) -> list[Trayecto]:
        statement = select(RouteORM)
        if flight_id is not None:
            statement = statement.where(RouteORM.flight_id == flight_id)
        orm_routes = self.session.execute(statement).scalars().all()
        return [self._to_domain(route) for route in orm_routes]

    def get_by_flight_id(self, flight_id: str) -> Optional[Trayecto]:
        statement = select(RouteORM).where(RouteORM.flight_id == flight_id)
        orm_route = self.session.execute(statement).scalar_one_or_none()
        if orm_route is None:
            return None
        return self._to_domain(orm_route)

    def delete(self, route_id: str) -> Trayecto:
        orm_route = self.session.get(RouteORM, route_id)
        if orm_route is None:
            raise RouteNotFoundError(f"Route with id {route_id} not found")
        self.session.delete(orm_route)
        self.session.commit()
        return self._to_domain(orm_route)

    def count(self) -> int:
        return self.session.query(RouteORM).count()

    def reset(self) -> None:
        self.session.query(RouteORM).delete()
        self.session.commit()

    @staticmethod
    def _to_domain(route: RouteORM) -> Trayecto:
        return Trayecto(
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
