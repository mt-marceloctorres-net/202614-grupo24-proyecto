from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import OfferNotFoundError


class DeleteOfferUseCase(BaseUseCase):
    """Caso de uso para eliminar una oferta."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(self, offer_id: str) -> None:
        """Elimina la oferta pedida.

        Comprueba primero que exista porque el adaptador borra en silencio
        cuando el id no está — un borrado idempotente es razonable a nivel de
        repositorio, pero el contrato exige distinguir el caso y responder 404.

        Raises:
            OfferNotFoundError: si no existe. El entrypoint lo traduce a 404.
        """
        if self.offer_repository.get_by_id(offer_id) is None:
            raise OfferNotFoundError(f"No existe una oferta con el id {offer_id}.")
        self.offer_repository.delete(offer_id)
