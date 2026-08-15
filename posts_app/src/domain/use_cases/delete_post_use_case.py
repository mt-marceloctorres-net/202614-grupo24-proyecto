from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import PostNotFoundError


class DeletePostUseCase(BaseUseCase):
    """Caso de uso para eliminar una publicación por id."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self, post_id: str) -> None:
        """Elimina la publicación con el id dado, o lanza si no existe."""
        deleted = self.post_repository.delete(post_id)
        if not deleted:
            raise PostNotFoundError(f"La publicación con id {post_id} no existe")
