from domain.use_cases.base_use_case import BaseUseCase


class CountRoutesUseCase(BaseUseCase):
    """Count all routes."""

    def __init__(self, repository):
        self.repository = repository

    def execute(self) -> int:
        return self.repository.count()
