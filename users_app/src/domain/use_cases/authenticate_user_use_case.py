import uuid
from datetime import datetime, timedelta, timezone

from config import Settings
from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidCredentialsError
from security import verify_password


class AuthenticateUserUseCase(BaseUseCase):
    """Caso de uso para generar un token de sesión."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, username: str, password: str) -> User:
        """Valida credenciales y genera un nuevo token para el usuario."""
        user = self.user_repository.get_by_username(username)
        if not user or not verify_password(password, user.password, user.salt):
            raise InvalidCredentialsError("Usuario o contraseña inválidos")

        user.token = str(uuid.uuid4())
        user.expireAt = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(
            minutes=Settings.token_expiration_minutes
        )
        return self.user_repository.update(user)
