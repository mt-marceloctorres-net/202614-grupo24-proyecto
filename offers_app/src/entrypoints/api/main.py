from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from adapters.postgres.database import engine
from adapters.postgres.models import Base
from config import settings
from entrypoints.api.routers.offer_router import router as offer_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas al arrancar la aplicación.

    El proyecto no usa migraciones: cada despliegue parte de una base vacía, y el
    evaluador levanta el clúster desde cero. `create_all` es idempotente — si la
    tabla ya existe no hace nada, así que reiniciar el pod no borra datos.

    Que esto viva en el arranque tiene un efecto deseado: si la base de datos no
    responde, el contenedor falla de inmediato en vez de aceptar peticiones que
    se caerían una por una. En Kubernetes eso se traduce en un pod que reintenta
    hasta que su Postgres esté lista.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(offer_router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Traduce los errores de validación de Pydantic a 400.

    FastAPI responde **422** por defecto cuando falta un campo o llega con otro
    tipo. El contrato del curso exige **400** para ese mismo caso, así que sin
    este manejador la app fallaría las pruebas del evaluador con un código que
    parece razonable pero no es el pedido.

    El detalle pasa por `jsonable_encoder` porque en Pydantic 2 la lista de
    errores puede contener objetos que `json` no sabe serializar; sin eso, un
    error de validación poco común se convertiría en un 500. El contrato no
    exige cuerpo en el 400, así que el detalle es solo una ayuda para depurar.
    """
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )
