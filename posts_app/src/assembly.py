from adapters.postgres.database import SessionLocal
from adapters.postgres.post_repository_adapter import PostgresPostRepositoryAdapter
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_posts_use_case import CountPostsUseCase
from domain.use_cases.create_post_use_case import CreatePostUseCase
from domain.use_cases.delete_post_use_case import DeletePostUseCase
from domain.use_cases.get_post_use_case import GetPostUseCase
from domain.use_cases.list_posts_use_case import ListPostsUseCase
from domain.use_cases.reset_posts_use_case import ResetPostsUseCase

repository: PostgresPostRepositoryAdapter = PostgresPostRepositoryAdapter(SessionLocal)


def build_create_post_use_case() -> BaseUseCase:
    """Caso de uso de creación de publicación."""
    return CreatePostUseCase(repository)


def build_list_posts_use_case() -> BaseUseCase:
    """Caso de uso de ver/filtrar publicaciones."""
    return ListPostsUseCase(repository)


def build_get_post_use_case() -> BaseUseCase:
    """Caso de uso de consulta de una publicación."""
    return GetPostUseCase(repository)


def build_delete_post_use_case() -> BaseUseCase:
    """Caso de uso de eliminación de una publicación."""
    return DeletePostUseCase(repository)


def build_count_posts_use_case() -> BaseUseCase:
    """Caso de uso de conteo de publicaciones."""
    return CountPostsUseCase(repository)


def build_reset_posts_use_case() -> BaseUseCase:
    """Caso de uso de borrado total de publicaciones."""
    return ResetPostsUseCase(repository)
