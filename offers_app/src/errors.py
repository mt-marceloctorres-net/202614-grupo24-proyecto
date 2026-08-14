class OfferNotFoundError(Exception):
    """Se lanza cuando no existe una oferta con el id consultado.

    El entrypoint la traduce a 404.
    """

    pass


class InvalidOfferValueError(Exception):
    """Se lanza cuando un campo tiene el formato correcto pero un valor inaceptable.

    Ejemplos del contrato: un tamaño de paquete que no es LARGE, MEDIUM ni SMALL,
    o una oferta negativa. El entrypoint la traduce a **412**, que es lo que
    distingue este caso del 400.

    No confundir con un error de formato (campo ausente, tipo equivocado): eso lo
    detecta Pydantic en el borde y se traduce a 400.
    """

    pass


class InvalidIdFormatError(Exception):
    """Se lanza cuando un identificador de la ruta no tiene formato uuid.

    El entrypoint la traduce a 400.
    """

    pass
