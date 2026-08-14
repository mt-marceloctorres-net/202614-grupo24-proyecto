from domain.models.route import Route


class GetRouteUseCase:
    """Get a specific route by ID."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self, route_id: str) -> Route | None:
        return self.repository.get_by_id(route_id)
