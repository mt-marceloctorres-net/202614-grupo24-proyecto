from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetOffersUseCase(BaseUseCase):
    """Caso de uso para vaciar la tabla de ofertas."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(self) -> None:
        """Elimina todas las ofertas.

        Existe para que el evaluador deje el servicio en un estado conocido
        antes de correr su colección de pruebas. Es destructivo por diseño y no
        pide confirmación: el contrato lo define así.
        """
        self.offer_repository.delete_all()
