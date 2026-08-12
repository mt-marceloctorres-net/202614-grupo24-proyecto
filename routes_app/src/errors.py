class RouteNotFoundError(Exception):
    """Raised when a route is not found."""


class RouteAlreadyExistsError(Exception):
    """Raised when a route with the same flight ID already exists."""


class InvalidRouteDatesError(Exception):
    """Raised when the route dates are invalid."""
