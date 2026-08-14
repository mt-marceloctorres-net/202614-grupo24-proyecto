from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

# Los endpoints de negocio (creación/consulta/eliminación de publicaciones)
# y los endpoints técnicos /posts/count y /posts/reset se agregan en la
# tarjeta #24, junto con el contrato de API confirmado. Este placeholder
# solo prueba que el servicio arranca y responde.
router = APIRouter(prefix="/posts")


@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"
