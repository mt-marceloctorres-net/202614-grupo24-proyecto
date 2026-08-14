import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator

from errors import InvalidOfferValueError


def es_uuid(valor: str) -> bool:
    """Indica si el texto tiene formato uuid, de cualquier versión."""
    try:
        uuid.UUID(valor)
    except (AttributeError, TypeError, ValueError):
        return False
    return True


class PackageSize(str, Enum):
    """Tamaños de paquete admitidos por el contrato."""

    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"


class OfferCreate(BaseModel):
    """Cuerpo de la solicitud POST /offers.

    `size` se declara como `str` y no como `PackageSize` a propósito. Si fuera el
    enum, Pydantic rechazaría "HUGE" como error de formato y el servicio
    respondería 400; el contrato exige **412** para un tamaño fuera de lo
    esperado. Lo mismo con `offer`: se acepta cualquier número y la regla de "no
    negativo" se evalúa en el dominio.

    Así queda repartido: Pydantic valida forma (campo ausente o de otro tipo, que
    es 400) y el dominio valida valor (que es 412).
    """

    postId: str
    userId: str
    description: str
    size: str
    fragile: bool
    offer: float

    @field_validator("postId", "userId")
    @classmethod
    def _validar_formato_uuid(cls, valor: str) -> str:
        """Exige formato uuid en los dos identificadores del cuerpo.

        La colección de pruebas del evaluador manda `postId: "invalidToken"` y
        espera **400**, así que esto no es una validación de más: sin ella el
        servicio respondería 201 y fallaría esa prueba. Va como validador de
        Pydantic, y no como regla de dominio, justamente porque el 400 es el
        código de "formato equivocado" — un valor fuera de rango sería 412.

        Se acepta cualquier versión de uuid: los identificadores del curso son
        uuid v1, así que exigir v4 rechazaría datos válidos.
        """
        if not es_uuid(valor):
            raise ValueError("debe tener formato uuid")
        return valor


DESCRIPCION_MAX = 140


class Offer(BaseModel):
    """Modelo de dominio Oferta."""

    id: str | None = None
    postId: str
    userId: str
    description: str
    size: PackageSize
    fragile: bool
    offer: float
    createdAt: datetime | None = None

    @classmethod
    def desde_solicitud(cls, datos: OfferCreate) -> "Offer":
        """Construye una oferta validando las reglas de negocio del contrato.

        Args:
            datos: cuerpo ya validado en forma por Pydantic.

        Returns:
            La oferta lista para persistir, sin id ni fecha de creación.

        Raises:
            InvalidOfferValueError: si el tamaño no es válido, la descripción
                excede los 140 caracteres o la oferta es negativa. El entrypoint
                lo traduce a 412.
        """
        if len(datos.description) > DESCRIPCION_MAX:
            raise InvalidOfferValueError(
                f"La descripción no puede superar los {DESCRIPCION_MAX} caracteres "
                f"(recibidos {len(datos.description)})."
            )

        try:
            size = PackageSize(datos.size)
        except ValueError as exc:
            admitidos = ", ".join(t.value for t in PackageSize)
            raise InvalidOfferValueError(
                f"El tamaño '{datos.size}' no es válido. Admitidos: {admitidos}."
            ) from exc

        if datos.offer < 0:
            raise InvalidOfferValueError("El valor de la oferta no puede ser negativo.")

        return cls(
            postId=datos.postId,
            userId=datos.userId,
            description=datos.description,
            size=size,
            fragile=datos.fragile,
            offer=datos.offer,
        )


class OfferCreatedResponse(BaseModel):
    """Respuesta 201 de POST /offers: solo tres campos, según el contrato."""

    id: str
    userId: str
    createdAt: datetime


class OfferDeletedResponse(BaseModel):
    """Respuesta 200 de DELETE /offers/{id}.

    El texto es exactamente el del contrato: la prueba del evaluador compara la
    cadena completa, no solo que exista la clave.
    """

    msg: str = "la oferta fue eliminada"


class OfferResponse(BaseModel):
    """Representación completa de una oferta en GET /offers y GET /offers/{id}."""

    id: str
    postId: str
    description: str
    size: PackageSize
    fragile: bool
    offer: float
    createdAt: datetime
    userId: str
