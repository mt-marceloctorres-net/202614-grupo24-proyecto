import pytest

from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.update_user_use_case import UpdateUserUseCase
from errors import InvalidRequestError, UserNotFoundError


def test_update_user_happy_path(user_repository, valid_user_data):
    """Actualiza solo los campos enviados."""
    created = CreateUserUseCase(user_repository).execute(**valid_user_data)
    use_case = UpdateUserUseCase(user_repository)

    use_case.execute(
        user_id=created.id,
        status=None,
        dni=None,
        fullName="Nuevo Nombre",
        phoneNumber=None,
    )

    updated = user_repository.get_by_id(created.id)
    assert updated.fullName == "Nuevo Nombre"
    assert updated.dni == valid_user_data["dni"]  # no se tocó


def test_update_user_without_any_field_raises(user_repository, valid_user_data):
    """Si no se envía ningún campo, es un error de negocio."""
    created = CreateUserUseCase(user_repository).execute(**valid_user_data)
    use_case = UpdateUserUseCase(user_repository)

    with pytest.raises(InvalidRequestError):
        use_case.execute(
            user_id=created.id, status=None, dni=None, fullName=None, phoneNumber=None
        )


def test_update_user_not_found_raises(user_repository):
    """Actualizar un usuario que no existe lanza error."""
    use_case = UpdateUserUseCase(user_repository)

    with pytest.raises(UserNotFoundError):
        use_case.execute(
            user_id="no-existe", status=None, dni="999", fullName=None, phoneNumber=None
        )
