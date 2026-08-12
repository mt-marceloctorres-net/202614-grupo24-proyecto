from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from config import Settings
from entrypoints.api.routers.route_router import router as route_router
from entrypoints.api.routers.route_router import (
    validation_exception_handler,
)

app = FastAPI(title=Settings.app_name())
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(route_router)
