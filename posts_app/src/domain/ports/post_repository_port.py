from abc import ABC, abstractmethod
from typing import Optional

from domain.models.post import Post


class PostRepositoryPort(ABC):
    """Interfaz del repositorio de publicaciones."""

    @abstractmethod
    def create(self, post: Post) -> Post:
        """Crea una nueva publicación."""
        pass

    @abstractmethod
    def get_by_id(self, post_id: str) -> Optional[Post]:
        """Obtiene una publicación por su id."""
        pass

    @abstractmethod
    def list(
        self,
        expire: Optional[bool] = None,
        route_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> list[Post]:
        """Lista publicaciones, filtrando (AND) por expiración/trayecto/dueño."""
        pass

    @abstractmethod
    def delete(self, post_id: str) -> bool:
        """Elimina una publicación por id. Retorna False si no existía."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Cuenta cuántas publicaciones hay almacenadas."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Elimina todas las publicaciones."""
        pass
