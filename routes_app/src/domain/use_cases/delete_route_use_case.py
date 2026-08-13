from domain.models.route import Route


class DeleteRouteUseCase:
    """Delete a route by ID."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self, route_id: str) -> Route:
        return self.repository.delete(route_id)
