from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from adapters.postgres.database import engine
from adapters.postgres.models import BaseORM
from config import Settings
from entrypoints.api.routers.route_router import router as route_router
from entrypoints.api.routers.route_router import (
    validation_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on real startup, not on module import (keeps unit tests DB-free)."""
    BaseORM.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=Settings.app_name(), lifespan=lifespan)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(route_router)
