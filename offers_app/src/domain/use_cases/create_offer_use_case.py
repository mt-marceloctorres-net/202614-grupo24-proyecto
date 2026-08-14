from domain.models.offer import Offer, OfferCreate
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CreateOfferUseCase(BaseUseCase):
    """Caso de uso para crear una oferta."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(self, datos: OfferCreate) -> Offer:
        """Crea una oferta a partir del cuerpo de la solicitud.

        Las reglas de negocio (tamaño admitido, oferta no negativa, longitud de
        la descripción) viven en `Offer.desde_solicitud`, que lanza
        `InvalidOfferValueError`. El caso de uso no las repite: si estuvieran en
        los dos lados, tarde o temprano una de las dos copias se quedaría atrás.

        El identificador y la fecha de creación los asigna el adaptador al
        persistir, así que la oferta que se devuelve ya viene con ambos.
        """
        offer = Offer.desde_solicitud(datos)
        return self.offer_repository.create(offer)
