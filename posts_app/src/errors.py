class PostNotFoundError(Exception):
    """Se lanza cuando no se encuentra una publicación."""

    pass


class InvalidExpirationError(Exception):
    """Se lanza cuando expireAt no es una fecha futura válida."""

    pass
