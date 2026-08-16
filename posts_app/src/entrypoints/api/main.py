from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from adapters.postgres.database import engine
from adapters.postgres.models import Base
from config import settings
from entrypoints.api.routers.post_router import router as post_router
from errors import InvalidExpirationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas al arrancar, no al importar el módulo.

    `Base.metadata.create_all` a nivel de módulo obligaría a tener una
    Postgres viva incluso para instanciar `TestClient` en pruebas unitarias.
    Se ejecuta aquí, en el arranque real de la aplicación.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(post_router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """El contrato del curso exige 400 para errores de validación, no el 422 por defecto de FastAPI.

    El detalle pasa por `jsonable_encoder` porque en Pydantic 2 la lista de
    errores puede contener objetos (como una excepción `ValueError` cruda de
    un `field_validator`) que `json.dumps` no sabe serializar; sin esto, un
    error de validación se convertiría en un 500 en vez de un 400.
    """
    return JSONResponse(
        status_code=400, content={"detail": jsonable_encoder(exc.errors())}
    )


@app.exception_handler(InvalidExpirationError)
def invalid_expiration_exception_handler(request: Request, exc: InvalidExpirationError):
    """El contrato de api_posts.md exige el cuerpo exacto {"msg": "..."} en el 412."""
    return JSONResponse(status_code=412, content={"msg": str(exc)})
