from adapters.postgres.database import SessionLocal
from adapters.postgres.user_repository_adapter import PostgresUserRepositoryAdapter
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.update_user_use_case import UpdateUserUseCase

repository: PostgresUserRepositoryAdapter = PostgresUserRepositoryAdapter(SessionLocal)


def build_create_user_use_case() -> BaseUseCase:
    """Caso de uso de creación de usuario."""
    return CreateUserUseCase(repository)


def build_update_user_use_case() -> BaseUseCase:
    """Caso de uso de actualización de usuario."""
    return UpdateUserUseCase(repository)


# Los `build_*_use_case` de autenticación y consulta se agregan en los
# issues #11 y #12.
