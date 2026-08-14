from typing import Optional

from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class GetOffersUseCase(BaseUseCase):
    """Caso de uso para listar ofertas, con filtros opcionales."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(
        self, post_id: Optional[str] = None, owner_id: Optional[str] = None
    ) -> list[Offer]:
        """Lista las ofertas que cumplen los filtros presentes.

        Los dos filtros son opcionales y se combinan con AND, según el contrato.
        Sin filtros devuelve todas las ofertas; con un filtro que no coincide con
        nada devuelve una lista vacía y **no** un 404: no encontrar resultados es
        una búsqueda exitosa con cero elementos.
        """
        return self.offer_repository.find(post_id=post_id, owner_id=owner_id)
