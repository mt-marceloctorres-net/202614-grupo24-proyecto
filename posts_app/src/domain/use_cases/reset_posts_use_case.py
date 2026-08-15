from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetPostsUseCase(BaseUseCase):
    """Caso de uso para eliminar todas las publicaciones."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self) -> None:
        """Elimina todas las publicaciones almacenadas."""
        self.post_repository.delete_all()
