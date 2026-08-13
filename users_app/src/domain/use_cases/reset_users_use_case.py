from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetUsersUseCase(BaseUseCase):
    """Caso de uso para borrar todos los usuarios."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self) -> None:
        """Elimina todos los usuarios. Idempotente."""
        self.user_repository.delete_all()
