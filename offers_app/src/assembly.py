from adapters.postgres.database import SessionLocal
from adapters.postgres.offer_repository_adapter import PostgresOfferRepositoryAdapter
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.create_offer_use_case import CreateOfferUseCase
from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from domain.use_cases.get_offer_use_case import GetOfferUseCase
from domain.use_cases.get_offers_use_case import GetOffersUseCase

# Único lugar del servicio donde se decide qué implementación concreta del
# puerto se usa. El dominio nunca importa el adaptador; si mañana la app
# cambiara de Postgres a otra cosa, este archivo sería el único que cambia.
repository: PostgresOfferRepositoryAdapter = PostgresOfferRepositoryAdapter(
    SessionLocal
)


def build_create_offer_use_case() -> BaseUseCase:
    """Caso de uso de creación de oferta."""
    return CreateOfferUseCase(repository)


def build_get_offers_use_case() -> BaseUseCase:
    """Caso de uso de listado y filtrado de ofertas."""
    return GetOffersUseCase(repository)


def build_get_offer_use_case() -> BaseUseCase:
    """Caso de uso de consulta de una oferta."""
    return GetOfferUseCase(repository)


def build_delete_offer_use_case() -> BaseUseCase:
    """Caso de uso de eliminación de una oferta."""
    return DeleteOfferUseCase(repository)
