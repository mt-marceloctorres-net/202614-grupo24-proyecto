class UserNotFoundError(Exception):
    """Se lanza cuando no se encuentra un usuario."""

    pass


class UserAlreadyExistsError(Exception):
    """Se lanza cuando el username o email ya existen."""

    pass
