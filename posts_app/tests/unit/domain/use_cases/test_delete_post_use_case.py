import pytest

from domain.use_cases.create_post_use_case import CreatePostUseCase
from domain.use_cases.delete_post_use_case import DeletePostUseCase
from errors import PostNotFoundError


def test_delete_post_found(post_repository, valid_post_data):
    """Elimina la publicación cuando el id existe."""
    created = CreatePostUseCase(post_repository).execute(**valid_post_data)

    DeletePostUseCase(post_repository).execute(post_id=created.id)

    assert post_repository.count() == 0
    assert post_repository.get_by_id(created.id) is None


def test_delete_post_not_found_raises(post_repository):
    """Lanza `PostNotFoundError` cuando el id no existe."""
    with pytest.raises(PostNotFoundError):
        DeletePostUseCase(post_repository).execute(post_id="no-existe")
