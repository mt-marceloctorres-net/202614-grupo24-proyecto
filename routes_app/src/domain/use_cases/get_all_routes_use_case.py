from domain.models.route import Route


class GetAllRoutesUseCase:
    """Get all routes, optionally filtered by flightId."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self, flight_id: str | None = None) -> list[Route]:
        return self.repository.get_all(flight_id)
