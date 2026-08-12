from domain.models.route import Trayecto


class DeleteRouteUseCase:
    """Delete a route by ID."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self, route_id: str) -> Trayecto:
        return self.repository.delete(route_id)
