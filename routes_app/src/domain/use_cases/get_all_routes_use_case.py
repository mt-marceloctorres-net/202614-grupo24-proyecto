from domain.models.route import Trayecto


class GetAllRoutesUseCase:
    """Get all routes, optionally filtered by flightId."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self, flight_id: str | None = None) -> list[Trayecto]:
        return self.repository.get_all(flight_id)
