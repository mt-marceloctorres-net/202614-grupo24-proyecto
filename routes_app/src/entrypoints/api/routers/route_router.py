from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, ConfigDict, Field

from assembly import (
    build_count_routes_use_case,
    build_create_route_use_case,
    build_delete_route_use_case,
    build_get_all_routes_use_case,
    build_get_route_use_case,
    build_reset_routes_use_case,
)
from domain.models.route import Route
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError, RouteNotFoundError

router = APIRouter(prefix="/routes")

count_routes_use_case_dep = Depends(build_count_routes_use_case)
reset_routes_use_case_dep = Depends(build_reset_routes_use_case)
get_all_routes_use_case_dep = Depends(build_get_all_routes_use_case)
get_route_use_case_dep = Depends(build_get_route_use_case)
delete_route_use_case_dep = Depends(build_delete_route_use_case)
create_route_use_case_dep = Depends(build_create_route_use_case)


class RouteCreate(BaseModel):
    """Input model for POST /routes: clients cannot set id/createdAt/updatedAt."""

    model_config = ConfigDict(extra="forbid")

    flightId: str = Field(..., min_length=1)
    sourceAirportCode: str = Field(..., min_length=1)
    sourceCountry: str = Field(..., min_length=1)
    destinyAirportCode: str = Field(..., min_length=1)
    destinyCountry: str = Field(..., min_length=1)
    bagCost: int = Field(..., gt=0)
    plannedStartDate: datetime
    plannedEndDate: datetime


class RouteCreateResponse(BaseModel):
    """201 response for POST /routes, per the api_routes.md contract."""

    id: str
    createdAt: datetime


class RouteDeletedResponse(BaseModel):
    """200 response for DELETE /routes/{id}, per the api_routes.md contract."""

    msg: str = "el trayecto fue eliminado"


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Map validation errors to HTTP 400 as required by the API contract."""
    return JSONResponse(
        status_code=400, content={"msg": jsonable_encoder(exc.errors())}
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Map HTTPException's default {"detail": ...} body to {"msg": ...} per the API contract."""
    return JSONResponse(status_code=exc.status_code, content={"msg": exc.detail})


@router.get("/ping", response_class=PlainTextResponse)
def health_check() -> str:
    """Simple health check endpoint used for the route app."""
    return "pong"


@router.get("/count")
def get_routes_count(
    use_case: BaseUseCase = count_routes_use_case_dep,
) -> dict[str, int]:
    """Return the total number of routes."""
    return {"count": use_case.execute()}


@router.post("/reset")
def reset_routes(
    use_case: BaseUseCase = reset_routes_use_case_dep,
) -> dict[str, str]:
    """Reset the route storage and return a status message."""
    return use_case.execute()


@router.get("", response_model=list[Route])
def get_routes(
    flight: str | None = Query(default=None, min_length=1),
    use_case: BaseUseCase = get_all_routes_use_case_dep,
) -> list[Route]:
    """Return a list of routes, optionally filtered by flightId."""
    return use_case.execute(flight)


@router.get("/{route_id}", response_model=Route)
def get_route(
    route_id: UUID,
    use_case: BaseUseCase = get_route_use_case_dep,
) -> Route:
    """Return a route by its UUID."""
    route = use_case.execute(str(route_id))
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.delete("/{route_id}", response_model=RouteDeletedResponse)
def delete_route(
    route_id: UUID,
    use_case: BaseUseCase = delete_route_use_case_dep,
) -> RouteDeletedResponse:
    """Delete a route by UUID."""
    try:
        use_case.execute(str(route_id))
    except RouteNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RouteDeletedResponse()


@router.post("", response_model=RouteCreateResponse, status_code=201)
def create_route(
    route_in: RouteCreate,
    use_case: BaseUseCase = create_route_use_case_dep,
) -> RouteCreateResponse:
    """Create a new route if the data is valid and unique."""
    try:
        created = use_case.execute(Route(**route_in.model_dump()))
        return RouteCreateResponse(id=created.id, createdAt=created.createdAt)
    except RouteAlreadyExistsError as exc:
        raise HTTPException(status_code=412, detail=str(exc)) from exc
    except InvalidRouteDatesError as exc:
        raise HTTPException(status_code=412, detail=str(exc)) from exc
