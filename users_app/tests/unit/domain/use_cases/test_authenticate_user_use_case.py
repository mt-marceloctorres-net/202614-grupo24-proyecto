import pytest

from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from errors import InvalidCredentialsError


def test_authenticate_happy_path(user_repository, valid_user_data):
    """Con credenciales correctas, genera un token y su vencimiento."""
    CreateUserUseCase(user_repository).execute(**valid_user_data)
    use_case = AuthenticateUserUseCase(user_repository)

    user = use_case.execute(
        username=valid_user_data["username"], password=valid_user_data["password"]
    )

    assert user.token is not None
    assert user.expireAt is not None


def test_authenticate_with_wrong_password_raises(user_repository, valid_user_data):
    """Con la contraseña incorrecta, no autentica."""
    CreateUserUseCase(user_repository).execute(**valid_user_data)
    use_case = AuthenticateUserUseCase(user_repository)

    with pytest.raises(InvalidCredentialsError):
        use_case.execute(username=valid_user_data["username"], password="incorrecta")


def test_authenticate_with_unknown_username_raises(user_repository):
    """Con un username que no existe, no autentica."""
    use_case = AuthenticateUserUseCase(user_repository)

    with pytest.raises(InvalidCredentialsError):
        use_case.execute(username="no-existe", password="lo-que-sea")
