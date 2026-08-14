from abc import ABC, abstractmethod
from typing import Optional

from domain.models.post import Post


class PostRepositoryPort(ABC):
    """Interfaz del repositorio de publicaciones.

    Cubre solo las operaciones que ya son seguras de anticipar en el scaffold
    (creación, consulta por id, y los endpoints técnicos /count y /reset).
    Los casos de uso de negocio (consulta filtrada, eliminación, etc.) y
    cualquier método adicional que el contrato de API requiera se agregan en
    la tarjeta #24, junto con el contrato confirmado.
    """

    @abstractmethod
    def create(self, post: Post) -> Post:
        """Crea una nueva publicación."""
        pass

    @abstractmethod
    def get_by_id(self, post_id: str) -> Optional[Post]:
        """Obtiene una publicación por su id."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Cuenta cuántas publicaciones hay almacenadas."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Elimina todas las publicaciones."""
        pass
