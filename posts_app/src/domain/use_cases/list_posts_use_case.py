from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ListPostsUseCase(BaseUseCase):
    """Caso de uso para ver y filtrar publicaciones."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(
        self,
        expire: bool | None = None,
        route: str | None = None,
        owner: str | None = None,
    ) -> list[Post]:
        """Retorna las publicaciones que cumplen (AND) los filtros dados."""
        return self.post_repository.list(expire=expire, route_id=route, owner_id=owner)
