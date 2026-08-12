from adapters.postgres.route_repository_adapter import PostgresRouteRepositoryAdapter
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.create_route_use_case import CreateRouteUseCase

repository = PostgresRouteRepositoryAdapter()


def build_route_repository() -> PostgresRouteRepositoryAdapter:
    """Return the route repository instance."""
    return repository


def build_create_route_use_case() -> BaseUseCase:
    """Build the create route use case."""
    return CreateRouteUseCase(repository)
