class UserNotFoundError(Exception):
    """Se lanza cuando no se encuentra un usuario."""

    pass


class UserAlreadyExistsError(Exception):
    """Se lanza cuando el username o email ya existen."""

    pass


class InvalidRequestError(Exception):
    """Se lanza cuando la solicitud no cumple una regla de negocio (no es un error de formato)."""

    pass


class InvalidCredentialsError(Exception):
    """Se lanza cuando el username o password no corresponden a ningún usuario."""

    pass


class InvalidTokenError(Exception):
    """Se lanza cuando el token no existe o ya venció."""

    pass
