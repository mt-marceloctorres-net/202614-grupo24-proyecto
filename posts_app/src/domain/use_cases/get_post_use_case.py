from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import PostNotFoundError


class GetPostUseCase(BaseUseCase):
    """Caso de uso para consultar una publicación por id."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self, post_id: str) -> Post:
        """Retorna la publicación con el id dado, o lanza si no existe."""
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(f"La publicación con id {post_id} no existe")
        return post
