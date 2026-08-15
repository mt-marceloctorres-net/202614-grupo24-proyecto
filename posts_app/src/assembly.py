from adapters.postgres.database import SessionLocal
from adapters.postgres.post_repository_adapter import PostgresPostRepositoryAdapter
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.create_post_use_case import CreatePostUseCase

repository: PostgresPostRepositoryAdapter = PostgresPostRepositoryAdapter(SessionLocal)


def build_create_post_use_case() -> BaseUseCase:
    """Caso de uso de creación de publicación."""
    return CreatePostUseCase(repository)
