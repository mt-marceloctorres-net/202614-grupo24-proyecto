from adapters.postgres.route_repository_adapter import PostgresRouteRepositoryAdapter

repository = PostgresRouteRepositoryAdapter()


def build_route_repository() -> PostgresRouteRepositoryAdapter:
    """Return the route repository instance."""
    return repository
