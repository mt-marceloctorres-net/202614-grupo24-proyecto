from datetime import datetime, timezone

from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidTokenError


class GetMeUseCase(BaseUseCase):
    """Caso de uso para consultar el usuario dueño de un token."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, token: str) -> User:
        """Retorna el usuario dueño del token, si es válido y no ha vencido."""
        user = self.user_repository.get_by_token(token)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if not user or not user.expireAt or user.expireAt < now:
            raise InvalidTokenError("El token no es válido o está vencido")
        return user
