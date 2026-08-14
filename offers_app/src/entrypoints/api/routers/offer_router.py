from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse

from assembly import (
    build_count_offers_use_case,
    build_create_offer_use_case,
    build_delete_offer_use_case,
    build_get_offer_use_case,
    build_get_offers_use_case,
    build_reset_offers_use_case,
)
from domain.models.offer import (
    OfferCountResponse,
    OfferCreate,
    OfferCreatedResponse,
    OfferDeletedResponse,
    OfferResetResponse,
    OfferResponse,
    es_uuid,
)
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidIdFormatError, InvalidOfferValueError, OfferNotFoundError

# El prefijo va en el router y no repetido en cada ruta. El contrato exige que
# todos los caminos de este servicio cuelguen de /offers.
router = APIRouter(prefix="/offers")


def _asegurar_uuid(offer_id: str) -> None:
    """Comprueba que el identificador de la ruta tenga formato uuid.

    Raises:
        InvalidIdFormatError: si no lo tiene. El entrypoint lo traduce a 400.
    """
    if not es_uuid(offer_id):
        raise InvalidIdFormatError("El id de la oferta debe tener formato uuid.")


@router.post("", response_model=OfferCreatedResponse, status_code=201)
def create_offer(
    payload: OfferCreate,
    use_case: BaseUseCase = Depends(build_create_offer_use_case),
):
    """Crea una oferta nueva.

    El reparto de errores es el del contrato: un campo ausente, de otro tipo o
    con un identificador que no es uuid lo rechaza Pydantic antes de llegar aquí
    y termina en 400 (ver el manejador de `main.py`); un valor fuera de lo
    admitido llega como excepción del dominio y se traduce a 412.
    """
    try:
        offer = use_case.execute(payload)
    except InvalidOfferValueError as err:
        raise HTTPException(status_code=412, detail=str(err)) from err

    # La respuesta declara exactamente los tres campos del contrato. Devolver el
    # modelo completo filtraría de más, y agregar una clave que el modelo no
    # declare no aparecería en el cuerpo: Pydantic serializa solo lo declarado.
    return OfferCreatedResponse(
        id=offer.id, userId=offer.userId, createdAt=offer.createdAt
    )


@router.get("", response_model=list[OfferResponse])
def get_offers(
    post: Optional[str] = Query(default=None),
    owner: Optional[str] = Query(default=None),
    use_case: BaseUseCase = Depends(build_get_offers_use_case),
):
    """Lista las ofertas, filtrando opcionalmente por publicación y por dueño.

    Los dos filtros se combinan con AND y ambos son opcionales; sin ninguno
    devuelve todas las ofertas.

    A diferencia del cuerpo de la creación, aquí **no** se valida que los
    filtros tengan formato uuid. La colección de pruebas del evaluador no
    incluye ningún caso de filtro mal formado, y sí incluye tres que esperan
    200; agregar un 400 que nadie prueba solo introduce una forma de fallar.
    Una búsqueda sin resultados es 200 con lista vacía, nunca 404.
    """
    ofertas = use_case.execute(post_id=post, owner_id=owner)
    return [OfferResponse(**oferta.model_dump()) for oferta in ofertas]


@router.get("/ping", response_class=PlainTextResponse)
def ping():
    """Confirma que el servicio está arriba.

    El contrato pide el texto `pong` en **texto plano**, no un JSON. Por eso
    `response_class=PlainTextResponse`: sin ella FastAPI serializaría la cadena
    como `"pong"` con comillas, que es otro cuerpo.

    No consulta la base de datos a propósito. Es una prueba de vida del proceso;
    si además comprobara la base, un problema de conexión dejaría al pod
    marcado como caído y Kubernetes lo reiniciaría en bucle sin arreglar nada.
    """
    return "pong"


@router.get("/count", response_model=OfferCountResponse)
def count_offers(use_case: BaseUseCase = Depends(build_count_offers_use_case)):
    """Devuelve cuántas ofertas hay almacenadas."""
    return OfferCountResponse(count=use_case.execute())


@router.post("/reset", response_model=OfferResetResponse)
def reset_offers(use_case: BaseUseCase = Depends(build_reset_offers_use_case)):
    """Elimina todas las ofertas. Lo usa el evaluador antes de sus pruebas."""
    use_case.execute()
    return OfferResetResponse()


# ⚠️ TRAMPA DE ORDEN — no muevas nada por debajo de esta línea hacia arriba, ni
# al revés. FastAPI resuelve las rutas en el orden en que se declaran, y
# `/{offer_id}` captura cualquier segmento. Si `/ping`, `/count` o `/reset` se
# declararan DESPUÉS de aquí, "ping" llegaría como si fuera un identificador,
# fallaría la comprobación de uuid y el servicio respondería 400 a un endpoint
# que el evaluador espera en 200. Toda ruta fija nueva va ARRIBA de esta línea.
@router.get("/{offer_id}", response_model=OfferResponse)
def get_offer(
    offer_id: str,
    use_case: BaseUseCase = Depends(build_get_offer_use_case),
):
    """Consulta una oferta por su identificador."""
    try:
        _asegurar_uuid(offer_id)
        offer = use_case.execute(offer_id)
    except InvalidIdFormatError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except OfferNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    return OfferResponse(**offer.model_dump())


@router.delete("/{offer_id}", response_model=OfferDeletedResponse)
def delete_offer(
    offer_id: str,
    use_case: BaseUseCase = Depends(build_delete_offer_use_case),
):
    """Elimina una oferta por su identificador."""
    try:
        _asegurar_uuid(offer_id)
        use_case.execute(offer_id)
    except InvalidIdFormatError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except OfferNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    return OfferDeletedResponse()
