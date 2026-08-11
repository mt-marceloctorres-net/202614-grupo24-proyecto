from adapters.postgres.database import SessionLocal
from adapters.postgres.user_repository_adapter import PostgresUserRepositoryAdapter
from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_users_use_case import CountUsersUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.get_me_use_case import GetMeUseCase
from domain.use_cases.reset_users_use_case import ResetUsersUseCase
from domain.use_cases.update_user_use_case import UpdateUserUseCase

repository: PostgresUserRepositoryAdapter = PostgresUserRepositoryAdapter(SessionLocal)


def build_create_user_use_case() -> BaseUseCase:
    """Caso de uso de creación de usuario."""
    return CreateUserUseCase(repository)


def build_update_user_use_case() -> BaseUseCase:
    """Caso de uso de actualización de usuario."""
    return UpdateUserUseCase(repository)


def build_authenticate_user_use_case() -> BaseUseCase:
    """Caso de uso de generación de token."""
    return AuthenticateUserUseCase(repository)


def build_get_me_use_case() -> BaseUseCase:
    """Caso de uso de consulta de /me."""
    return GetMeUseCase(repository)


def build_count_users_use_case() -> BaseUseCase:
    """Caso de uso de conteo de usuarios."""
    return CountUsersUseCase(repository)


def build_reset_users_use_case() -> BaseUseCase:
    """Caso de uso de borrado total de usuarios."""
    return ResetUsersUseCase(repository)
