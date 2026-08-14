from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import OfferNotFoundError


class GetOfferUseCase(BaseUseCase):
    """Caso de uso para consultar una oferta por su identificador."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(self, offer_id: str) -> Offer:
        """Devuelve la oferta pedida.

        Raises:
            OfferNotFoundError: si no existe. El entrypoint lo traduce a 404.
        """
        offer = self.offer_repository.get_by_id(offer_id)
        if offer is None:
            raise OfferNotFoundError(f"No existe una oferta con el id {offer_id}.")
        return offer
