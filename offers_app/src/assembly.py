from adapters.postgres.database import SessionLocal
from adapters.postgres.offer_repository_adapter import PostgresOfferRepositoryAdapter
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.create_offer_use_case import CreateOfferUseCase

# Único lugar del servicio donde se decide qué implementación concreta del
# puerto se usa. El dominio nunca importa el adaptador; si mañana la app
# cambiara de Postgres a otra cosa, este archivo sería el único que cambia.
repository: PostgresOfferRepositoryAdapter = PostgresOfferRepositoryAdapter(
    SessionLocal
)


def build_create_offer_use_case() -> BaseUseCase:
    """Caso de uso de creación de oferta."""
    return CreateOfferUseCase(repository)
