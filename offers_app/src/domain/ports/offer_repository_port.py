from abc import ABC, abstractmethod
from typing import Optional

from domain.models.offer import Offer


class OfferRepositoryPort(ABC):
    """Interfaz del repositorio de ofertas.

    El dominio depende de esta abstracción, no de SQLAlchemy. El adaptador de
    Postgres la implementa, y las pruebas unitarias la sustituyen por un doble en
    memoria — por eso no hace falta una base de datos viva para probar los casos
    de uso.
    """

    @abstractmethod
    def create(self, offer: Offer) -> Offer:
        """Persiste una oferta nueva y devuelve la versión con id y fecha."""
        pass

    @abstractmethod
    def get_by_id(self, offer_id: str) -> Optional[Offer]:
        """Obtiene una oferta por su id, o None si no existe."""
        pass

    @abstractmethod
    def find(
        self, post_id: Optional[str] = None, owner_id: Optional[str] = None
    ) -> list[Offer]:
        """Lista ofertas filtrando por publicación y/o dueño.

        Los filtros son opcionales y se combinan con AND. Sin filtros devuelve
        todas las ofertas.
        """
        pass

    @abstractmethod
    def delete(self, offer_id: str) -> None:
        """Elimina una oferta existente."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Cuenta cuántas ofertas hay almacenadas."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Elimina todas las ofertas."""
        pass
