from fastapi import APIRouter, Depends, HTTPException

from assembly import build_create_offer_use_case
from domain.models.offer import OfferCreate, OfferCreatedResponse
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidOfferValueError

# El prefijo va en el router y no repetido en cada ruta. El contrato exige que
# todos los caminos de este servicio cuelguen de /offers, incluidos los técnicos
# (/offers/ping, /offers/reset, /offers/count), que llegan en el issue #33.
router = APIRouter(prefix="/offers")


@router.post("", response_model=OfferCreatedResponse, status_code=201)
def create_offer(
    payload: OfferCreate,
    use_case: BaseUseCase = Depends(build_create_offer_use_case),
):
    """Crea una oferta nueva.

    El reparto de errores es el del contrato: un campo ausente o de otro tipo lo
    rechaza Pydantic antes de llegar aquí y termina en 400 (ver el manejador de
    `main.py`); un valor fuera de lo admitido llega como excepción del dominio y
    se traduce a 412.
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
