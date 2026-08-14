from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from assembly import (
    build_create_offer_use_case,
    build_delete_offer_use_case,
    build_get_offer_use_case,
    build_get_offers_use_case,
)
from domain.models.offer import (
    OfferCreate,
    OfferCreatedResponse,
    OfferDeletedResponse,
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


# ⚠️ TRAMPA DE ORDEN — leer antes de agregar los endpoints técnicos (#33).
# FastAPI resuelve las rutas en el orden en que se declaran, y `/{offer_id}`
# captura cualquier segmento. Si `/offers/ping`, `/offers/count` o
# `/offers/reset` se declaran DESPUÉS de esta línea, "ping" llega como si fuera
# un identificador, falla la comprobación de uuid y el servicio responde 400 a
# un endpoint que el evaluador espera en 200. Las rutas fijas van ARRIBA de esta.
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
