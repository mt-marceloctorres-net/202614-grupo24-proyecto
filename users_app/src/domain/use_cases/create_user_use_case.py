import uuid

from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import UserAlreadyExistsError
from security import hash_password


class CreateUserUseCase(BaseUseCase):
    """Caso de uso para crear un usuario."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(
        self,
        username: str,
        password: str,
        email: str,
        dni: str | None,
        fullName: str | None,
        phoneNumber: str | None,
    ) -> User:
        """Crea un usuario nuevo, validando unicidad y cifrando la contraseña."""
        if self.user_repository.get_by_username_or_email(username, email):
            raise UserAlreadyExistsError("El username o el email ya existen")

        password_hash, salt = hash_password(password)

        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            dni=dni,
            fullName=fullName,
            phoneNumber=phoneNumber,
            password=password_hash,
            salt=salt,
        )
        return self.user_repository.create(user)
