import uuid
from datetime import datetime, timedelta, timezone

from domain.models.post import Post
from domain.use_cases.list_posts_use_case import ListPostsUseCase


def _make_post(
    post_repository, route_id="r1", user_id="u1", expire_delta=timedelta(days=1)
):
    """Inserta una publicación directamente en el repositorio, sin pasar por el caso de
    uso de creación: permite fabricar publicaciones ya expiradas (`CreatePostUseCase`
    lo prohíbe) para poder probar el filtro `expire`.
    """
    post = Post(
        id=str(uuid.uuid4()),
        routeId=route_id,
        userId=user_id,
        expireAt=datetime.now(timezone.utc).replace(tzinfo=None) + expire_delta,
    )
    return post_repository.create(post)


def test_list_posts_empty_repository_returns_empty_list(post_repository):
    """Sin publicaciones almacenadas, la lista es vacía."""
    posts = ListPostsUseCase(post_repository).execute()

    assert posts == []


def test_list_posts_without_filters_returns_all(post_repository):
    """Sin filtros, se retornan todas las publicaciones."""
    _make_post(post_repository, route_id="r1", user_id="u1")
    _make_post(post_repository, route_id="r2", user_id="u2")

    posts = ListPostsUseCase(post_repository).execute()

    assert len(posts) == 2


def test_list_posts_filter_by_route(post_repository):
    """El filtro `route` retorna solo las publicaciones de ese trayecto."""
    _make_post(post_repository, route_id="r1", user_id="u1")
    _make_post(post_repository, route_id="r2", user_id="u2")

    posts = ListPostsUseCase(post_repository).execute(route="r1")

    assert len(posts) == 1
    assert posts[0].routeId == "r1"


def test_list_posts_filter_by_owner(post_repository):
    """El filtro `owner` retorna solo las publicaciones de ese dueño."""
    _make_post(post_repository, route_id="r1", user_id="u1")
    _make_post(post_repository, route_id="r2", user_id="u2")

    posts = ListPostsUseCase(post_repository).execute(owner="u2")

    assert len(posts) == 1
    assert posts[0].userId == "u2"


def test_list_posts_filter_by_expire_true_returns_only_expired(post_repository):
    """El filtro `expire=True` retorna solo publicaciones ya expiradas."""
    _make_post(post_repository, expire_delta=timedelta(days=-1))
    _make_post(post_repository, expire_delta=timedelta(days=1))

    posts = ListPostsUseCase(post_repository).execute(expire=True)

    assert len(posts) == 1


def test_list_posts_filter_by_expire_false_returns_only_active(post_repository):
    """El filtro `expire=False` retorna solo publicaciones vigentes."""
    _make_post(post_repository, expire_delta=timedelta(days=-1))
    _make_post(post_repository, expire_delta=timedelta(days=1))

    posts = ListPostsUseCase(post_repository).execute(expire=False)

    assert len(posts) == 1


def test_list_posts_combined_filters(post_repository):
    """Los filtros se combinan con AND, no OR."""
    _make_post(post_repository, route_id="r1", user_id="u1")
    _make_post(post_repository, route_id="r1", user_id="u2")
    _make_post(post_repository, route_id="r2", user_id="u1")

    posts = ListPostsUseCase(post_repository).execute(route="r1", owner="u1")

    assert len(posts) == 1
    assert posts[0].routeId == "r1"
    assert posts[0].userId == "u1"
