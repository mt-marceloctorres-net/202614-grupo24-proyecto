from datetime import datetime, timezone
from uuid import uuid4

from domain.models.route import Route
from errors import InvalidRouteDatesError, RouteAlreadyExistsError


def _as_aware_utc(value: datetime) -> datetime:
    """Treat naive datetimes as UTC so they can be compared with aware ones."""
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


class CreateRouteUseCase:
    """Create a route with validation rules defined by the domain."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self, route: Route) -> Route:
        """Validate and create a route."""
        if self.repository.get_by_flight_id(route.flightId) is not None:
            raise RouteAlreadyExistsError(
                f"Route with flightId {route.flightId} already exists"
            )

        now = datetime.now(timezone.utc)
        start = _as_aware_utc(route.plannedStartDate)
        end = _as_aware_utc(route.plannedEndDate)
        if start <= now or end <= now:
            raise InvalidRouteDatesError("Dates must be in the future")

        if start >= end:
            raise InvalidRouteDatesError(
                "plannedStartDate must be before plannedEndDate"
            )

        if route.createdAt is None:
            route.createdAt = now
        if route.updatedAt is None:
            route.updatedAt = route.createdAt

        if route.id is None:
            route.id = str(uuid4())

        return self.repository.create(route)
