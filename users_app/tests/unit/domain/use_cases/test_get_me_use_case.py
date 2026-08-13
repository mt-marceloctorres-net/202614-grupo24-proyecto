from datetime import datetime, timedelta, timezone

import pytest

from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.get_me_use_case import GetMeUseCase
from errors import InvalidTokenError


def test_get_me_happy_path(user_repository, valid_user_data):
    """Con un token vigente, retorna el usuario dueño."""
    CreateUserUseCase(user_repository).execute(**valid_user_data)
    authenticated = AuthenticateUserUseCase(user_repository).execute(
        username=valid_user_data["username"], password=valid_user_data["password"]
    )
    use_case = GetMeUseCase(user_repository)

    user = use_case.execute(token=authenticated.token)

    assert user.username == valid_user_data["username"]


def test_get_me_with_unknown_token_raises(user_repository):
    """Un token que no existe no es válido."""
    use_case = GetMeUseCase(user_repository)

    with pytest.raises(InvalidTokenError):
        use_case.execute(token="token-inexistente")


def test_get_me_with_expired_token_raises(user_repository, valid_user_data):
    """Un token vencido no es válido."""
    created = CreateUserUseCase(user_repository).execute(**valid_user_data)
    created.token = "un-token"
    created.expireAt = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(
        minutes=1
    )
    user_repository.update(created)
    use_case = GetMeUseCase(user_repository)

    with pytest.raises(InvalidTokenError):
        use_case.execute(token="un-token")
