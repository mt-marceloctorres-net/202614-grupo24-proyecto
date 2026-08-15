from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountPostsUseCase(BaseUseCase):
    """Caso de uso para contar las publicaciones almacenadas."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self) -> int:
        """Retorna la cantidad de publicaciones almacenadas."""
        return self.post_repository.count()
