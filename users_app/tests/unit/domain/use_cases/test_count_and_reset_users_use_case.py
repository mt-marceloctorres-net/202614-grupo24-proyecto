from domain.use_cases.count_users_use_case import CountUsersUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.reset_users_use_case import ResetUsersUseCase


def test_count_users(user_repository, valid_user_data):
    """Cuenta correctamente los usuarios almacenados."""
    assert CountUsersUseCase(user_repository).execute() == 0

    CreateUserUseCase(user_repository).execute(**valid_user_data)

    assert CountUsersUseCase(user_repository).execute() == 1


def test_reset_users(user_repository, valid_user_data):
    """Elimina todos los usuarios."""
    CreateUserUseCase(user_repository).execute(**valid_user_data)

    ResetUsersUseCase(user_repository).execute()

    assert CountUsersUseCase(user_repository).execute() == 0
