from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountUsersUseCase(BaseUseCase):
    """Caso de uso para contar cuántos usuarios hay almacenados."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self) -> int:
        """Retorna la cantidad de usuarios."""
        return self.user_repository.count()
