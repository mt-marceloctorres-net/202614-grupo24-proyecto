from domain.models.user import UserStatus
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidRequestError, UserNotFoundError


class UpdateUserUseCase(BaseUseCase):
    """Caso de uso para actualizar los datos públicos de un usuario."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(
        self,
        user_id: str,
        status: UserStatus | None,
        dni: str | None,
        fullName: str | None,
        phoneNumber: str | None,
    ) -> None:
        """Actualiza solo los campos recibidos; exige al menos uno."""
        if status is None and dni is None and fullName is None and phoneNumber is None:
            raise InvalidRequestError("Debe enviar al menos un campo para actualizar")

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario con id {user_id} no existe")

        if status is not None:
            user.status = status
        if dni is not None:
            user.dni = dni
        if fullName is not None:
            user.fullName = fullName
        if phoneNumber is not None:
            user.phoneNumber = phoneNumber

        self.user_repository.update(user)
