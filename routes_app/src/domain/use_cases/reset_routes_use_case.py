from domain.use_cases.base_use_case import BaseUseCase


class ResetRoutesUseCase(BaseUseCase):
    """Reset all routes in the system."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self) -> dict[str, str]:
        self.repository.reset()
        return {"msg": "Routes reset successfully"}
