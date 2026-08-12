from abc import ABC, abstractmethod

from domain.models.route import Trayecto


class RouteRepositoryPort(ABC):
    """Repository interface for routes."""

    @abstractmethod
    def create(self, route: Trayecto) -> Trayecto:
        """Persist a new route."""

    @abstractmethod
    def get_by_id(self, route_id: str) -> Trayecto | None:
        """Get a route by ID."""

    @abstractmethod
    def get_all(self, flight_id: str | None = None) -> list[Trayecto]:
        """Get all routes, optionally filtering by flight ID."""

    @abstractmethod
    def get_by_flight_id(self, flight_id: str) -> Trayecto | None:
        """Get a route by flight ID."""

    @abstractmethod
    def delete(self, route_id: str) -> Trayecto:
        """Delete a route by ID."""

    @abstractmethod
    def count(self) -> int:
        """Count all routes."""

    @abstractmethod
    def reset(self) -> None:
        """Remove all routes."""
