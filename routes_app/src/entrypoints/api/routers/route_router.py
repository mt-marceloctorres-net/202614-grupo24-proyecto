from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

from assembly import (
    build_create_route_use_case,
    build_delete_route_use_case,
    build_get_all_routes_use_case,
    build_get_route_use_case,
)
from domain.models.route import Trayecto
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError, RouteNotFoundError

router = APIRouter(prefix="/routes")


@router.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Map validation errors to HTTP 400 as required by the API contract."""
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


@router.get("/ping", response_class=PlainTextResponse)
def health_check() -> str:
    """Simple health check endpoint used for the route app."""
    return "pong"


@router.get("", response_model=list[Trayecto])
def get_routes(
    flight: str | None = Query(default=None, min_length=1),
    use_case: BaseUseCase = Depends(build_get_all_routes_use_case),
) -> list[Trayecto]:
    """Return a list of routes, optionally filtered by flightId."""
    return use_case.execute(flight)


@router.get("/{route_id}", response_model=Trayecto)
def get_route(
    route_id: UUID, use_case: BaseUseCase = Depends(build_get_route_use_case)
) -> Trayecto:
    """Return a route by its UUID."""
    route = use_case.execute(str(route_id))
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.delete("/{route_id}", response_model=Trayecto)
def delete_route(
    route_id: UUID, use_case: BaseUseCase = Depends(build_delete_route_use_case)
) -> Trayecto:
    """Delete a route by UUID."""
    try:
        return use_case.execute(str(route_id))
    except RouteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


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
