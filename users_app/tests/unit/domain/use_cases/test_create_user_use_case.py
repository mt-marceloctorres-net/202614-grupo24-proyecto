import pytest

from domain.use_cases.create_user_use_case import CreateUserUseCase
from errors import UserAlreadyExistsError


def test_create_user_happy_path(user_repository, valid_user_data):
    """Crea un usuario nuevo y le asigna un id."""
    use_case = CreateUserUseCase(user_repository)

    user = use_case.execute(**valid_user_data)

    assert user.id is not None
    assert user.username == valid_user_data["username"]
    assert user.password != valid_user_data["password"]  # queda cifrada
    assert user.salt is not None


def test_create_user_with_duplicate_username_raises(user_repository, valid_user_data):
    """No se puede crear un usuario con un username que ya existe."""
    use_case = CreateUserUseCase(user_repository)
    use_case.execute(**valid_user_data)

    with pytest.raises(UserAlreadyExistsError):
        use_case.execute(**{**valid_user_data, "email": "otro@example.com"})


def test_create_user_with_duplicate_email_raises(user_repository, valid_user_data):
    """No se puede crear un usuario con un email que ya existe."""
    use_case = CreateUserUseCase(user_repository)
    use_case.execute(**valid_user_data)

    with pytest.raises(UserAlreadyExistsError):
        use_case.execute(**{**valid_user_data, "username": "otro_user"})
