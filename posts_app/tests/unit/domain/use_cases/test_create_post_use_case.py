from datetime import datetime, timedelta, timezone

import pytest

from domain.use_cases.create_post_use_case import CreatePostUseCase
from errors import InvalidExpirationError


def test_create_post_happy_path(post_repository, valid_post_data):
    """Crea una publicación nueva y le asigna un id."""
    use_case = CreatePostUseCase(post_repository)

    post = use_case.execute(**valid_post_data)

    assert post.id is not None
    assert post.routeId == valid_post_data["routeId"]
    assert post.userId == valid_post_data["userId"]
    assert post_repository.count() == 1


def test_create_post_with_past_expire_at_raises(post_repository, valid_post_data):
    """No se puede crear una publicación cuya fecha de expiración ya pasó."""
    use_case = CreatePostUseCase(post_repository)
    past = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)

    with pytest.raises(InvalidExpirationError):
        use_case.execute(
            routeId=valid_post_data["routeId"],
            userId=valid_post_data["userId"],
            expireAt=past,
        )
    assert post_repository.count() == 0


def test_create_post_with_expire_at_equal_now_raises(post_repository, valid_post_data):
    """La fecha de expiración debe ser estrictamente futura, no basta con ser 'ahora'."""
    use_case = CreatePostUseCase(post_repository)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with pytest.raises(InvalidExpirationError):
        use_case.execute(
            routeId=valid_post_data["routeId"],
            userId=valid_post_data["userId"],
            expireAt=now,
        )


def test_create_post_normalizes_timezone_aware_expire_at(
    post_repository, valid_post_data
):
    """Un `expireAt` con timezone se normaliza a UTC sin tzinfo antes de guardarse."""
    use_case = CreatePostUseCase(post_repository)
    future_aware = datetime.now(timezone.utc) + timedelta(days=1)

    post = use_case.execute(
        routeId=valid_post_data["routeId"],
        userId=valid_post_data["userId"],
        expireAt=future_aware,
    )

    assert post.expireAt.tzinfo is None


def test_create_post_with_timezone_in_the_past_raises(post_repository, valid_post_data):
    """Una fecha con timezone que, normalizada, queda en el pasado también debe fallar."""
    use_case = CreatePostUseCase(post_repository)
    past_aware = datetime.now(timezone.utc) - timedelta(days=1)

    with pytest.raises(InvalidExpirationError):
        use_case.execute(
            routeId=valid_post_data["routeId"],
            userId=valid_post_data["userId"],
            expireAt=past_aware,
        )
