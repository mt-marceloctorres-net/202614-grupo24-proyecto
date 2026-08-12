from datetime import datetime, timezone
from uuid import uuid4

from domain.models.route import Trayecto
from errors import InvalidRouteDatesError, RouteAlreadyExistsError


class CreateRouteUseCase:
    """Create a route with validation rules defined by the domain."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self, route: Trayecto) -> Trayecto:
        """Validate and create a route."""
        if self.repository.get_by_flight_id(route.flightId) is not None:
            raise RouteAlreadyExistsError(f"Route with flightId {route.flightId} already exists")

        now = datetime.now(timezone.utc)
        if route.plannedStartDate <= now or route.plannedEndDate <= now:
            raise InvalidRouteDatesError("Dates must be in the future")

        if route.plannedStartDate >= route.plannedEndDate:
            raise InvalidRouteDatesError("plannedStartDate must be before plannedEndDate")

        if route.createdAt is None:
            route.createdAt = now
        if route.updatedAt is None:
            route.updatedAt = route.createdAt

        if route.id is None:
            route.id = str(uuid4())

        return self.repository.create(route)
