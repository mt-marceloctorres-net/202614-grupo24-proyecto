from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from adapters.postgres.database import engine
from adapters.postgres.models import Base
from config import Settings
from entrypoints.api.routers.user_router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=Settings.app_name)
app.include_router(user_router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """El contrato del curso exige 400 para errores de validación, no el 422 por defecto de FastAPI."""
    return JSONResponse(status_code=400, content={"detail": exc.errors()})
