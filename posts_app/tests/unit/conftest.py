from datetime import datetime, timedelta, timezone
from typing import Optional

import pytest

from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort


class FakePostRepository(PostRepositoryPort):
    """Repositorio en memoria para pruebas unitarias, sin depender de Postgres."""

    def __init__(self):
        self.posts: dict[str, Post] = {}

    def create(self, post: Post) -> Post:
        self.posts[post.id] = post
        return post

    def get_by_id(self, post_id: str) -> Optional[Post]:
        return self.posts.get(post_id)

    def list(
        self,
        expire: Optional[bool] = None,
        route_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> list[Post]:
        results = list(self.posts.values())
        if route_id is not None:
            results = [post for post in results if post.routeId == route_id]
        if owner_id is not None:
            results = [post for post in results if post.userId == owner_id]
        if expire is not None:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            if expire:
                results = [post for post in results if post.expireAt <= now]
            else:
                results = [post for post in results if post.expireAt > now]
        return results

    def delete(self, post_id: str) -> bool:
        if post_id in self.posts:
            del self.posts[post_id]
            return True
        return False

    def count(self) -> int:
        return len(self.posts)

    def delete_all(self) -> None:
        self.posts.clear()


@pytest.fixture
def post_repository() -> FakePostRepository:
    """Repositorio en memoria vacío para cada prueba."""
    return FakePostRepository()


@pytest.fixture
def future_expire_at() -> datetime:
    """Fecha de expiración válida en el futuro (sin tzinfo, como la normaliza el caso de uso)."""
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=1)


@pytest.fixture
def valid_post_data(future_expire_at):
    """Datos válidos para crear una publicación."""
    return {
        "routeId": "11111111-1111-1111-1111-111111111111",
        "userId": "22222222-2222-2222-2222-222222222222",
        "expireAt": future_expire_at,
    }
