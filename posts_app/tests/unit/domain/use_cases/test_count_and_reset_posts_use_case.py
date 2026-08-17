from domain.use_cases.count_posts_use_case import CountPostsUseCase
from domain.use_cases.create_post_use_case import CreatePostUseCase
from domain.use_cases.reset_posts_use_case import ResetPostsUseCase


def test_count_posts(post_repository, valid_post_data):
    """Cuenta correctamente las publicaciones almacenadas."""
    assert CountPostsUseCase(post_repository).execute() == 0

    CreatePostUseCase(post_repository).execute(**valid_post_data)

    assert CountPostsUseCase(post_repository).execute() == 1


def test_reset_posts(post_repository, valid_post_data):
    """Elimina todas las publicaciones almacenadas."""
    CreatePostUseCase(post_repository).execute(**valid_post_data)

    ResetPostsUseCase(post_repository).execute()

    assert CountPostsUseCase(post_repository).execute() == 0
