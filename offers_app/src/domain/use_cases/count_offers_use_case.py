from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountOffersUseCase(BaseUseCase):
    """Caso de uso para contar las ofertas almacenadas."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(self) -> int:
        """Devuelve cuántas ofertas hay en la base de datos."""
        return self.offer_repository.count()
