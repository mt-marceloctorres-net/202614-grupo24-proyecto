import pytest

from domain.use_cases.create_post_use_case import CreatePostUseCase
from domain.use_cases.get_post_use_case import GetPostUseCase
from errors import PostNotFoundError


def test_get_post_found(post_repository, valid_post_data):
    """Retorna la publicación cuando el id existe."""
    created = CreatePostUseCase(post_repository).execute(**valid_post_data)

    result = GetPostUseCase(post_repository).execute(post_id=created.id)

    assert result.id == created.id
    assert result.routeId == valid_post_data["routeId"]
    assert result.userId == valid_post_data["userId"]


def test_get_post_not_found_raises(post_repository):
    """Lanza `PostNotFoundError` cuando el id no existe."""
    with pytest.raises(PostNotFoundError):
        GetPostUseCase(post_repository).execute(post_id="no-existe")
