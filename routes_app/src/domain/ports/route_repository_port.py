from abc import ABC, abstractmethod

from domain.models.route import Route


class RouteRepositoryPort(ABC):
    """Repository interface for routes."""

    @abstractmethod
    def create(self, route: Route) -> Route:
        """Persist a new route."""

    @abstractmethod
    def get_by_id(self, route_id: str) -> Route | None:
        """Get a route by ID."""

    @abstractmethod
    def get_all(self, flight_id: str | None = None) -> list[Route]:
        """Get all routes, optionally filtering by flight ID."""

    @abstractmethod
    def get_by_flight_id(self, flight_id: str) -> Route | None:
        """Get a route by flight ID."""

    @abstractmethod
    def delete(self, route_id: str) -> Route:
        """Delete a route by ID."""

    @abstractmethod
    def count(self) -> int:
        """Count all routes."""

    @abstractmethod
    def reset(self) -> None:
        """Remove all routes."""
