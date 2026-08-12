from domain.models.route import Trayecto


class GetRouteUseCase:
    """Get a specific route by ID."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self, route_id: str) -> Trayecto | None:
        return self.repository.get_by_id(route_id)
