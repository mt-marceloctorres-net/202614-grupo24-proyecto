from adapters.postgres.route_repository_adapter import PostgresRouteRepositoryAdapter
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_routes_use_case import CountRoutesUseCase
from domain.use_cases.create_route_use_case import CreateRouteUseCase
from domain.use_cases.delete_route_use_case import DeleteRouteUseCase
from domain.use_cases.get_all_routes_use_case import GetAllRoutesUseCase
from domain.use_cases.get_route_use_case import GetRouteUseCase
from domain.use_cases.reset_routes_use_case import ResetRoutesUseCase

repository = PostgresRouteRepositoryAdapter()


def build_route_repository() -> PostgresRouteRepositoryAdapter:
    """Return the route repository instance."""
    return repository


def build_create_route_use_case() -> BaseUseCase:
    """Build the create route use case."""
    return CreateRouteUseCase(repository)


def build_get_all_routes_use_case() -> BaseUseCase:
    """Build the use case for retrieving routes."""
    return GetAllRoutesUseCase(repository)


def build_get_route_use_case() -> BaseUseCase:
    """Build the use case for retrieving a single route."""
    return GetRouteUseCase(repository)


def build_delete_route_use_case() -> BaseUseCase:
    """Build the use case for deleting a route."""
    return DeleteRouteUseCase(repository)


def build_count_routes_use_case() -> BaseUseCase:
    """Build the use case for counting routes."""
    return CountRoutesUseCase(repository)


def build_reset_routes_use_case() -> BaseUseCase:
    """Build the use case for resetting routes."""
    return ResetRoutesUseCase(repository)
