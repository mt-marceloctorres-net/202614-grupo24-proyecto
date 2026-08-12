from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

from assembly import build_create_route_use_case
from domain.models.route import Trayecto
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError

router = APIRouter(prefix="/routes")


@router.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Map validation errors to HTTP 400 as required by the API contract."""
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


@router.get("/ping", response_class=PlainTextResponse)
def health_check() -> str:
    """Simple health check endpoint used for the route app."""
    return "pong"


@router.post("", response_model=Trayecto, status_code=201)
def create_route(
    route: Trayecto, use_case: BaseUseCase = Depends(build_create_route_use_case)
) -> Trayecto:
    """Create a new route if the data is valid and unique."""
    try:
        route.createdAt = route.createdAt or datetime.utcnow()
        route.updatedAt = route.updatedAt or route.createdAt
        return use_case.execute(route)
    except RouteAlreadyExistsError as exc:
        raise HTTPException(status_code=412, detail=str(exc)) from exc
    except InvalidRouteDatesError as exc:
        raise HTTPException(status_code=412, detail=str(exc)) from exc
