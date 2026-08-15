import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from assembly import (
    build_count_posts_use_case,
    build_create_post_use_case,
    build_delete_post_use_case,
    build_get_post_use_case,
    build_list_posts_use_case,
    build_reset_posts_use_case,
)
from domain.use_cases.base_use_case import BaseUseCase
from errors import PostNotFoundError

router = APIRouter(prefix="/posts")


def _validate_uuid_format(post_id: str) -> None:
    """El contrato exige 400 si el id no tiene formato uuid (no si no existe)."""
    try:
        uuid.UUID(post_id)
    except ValueError as err:
        raise HTTPException(
            status_code=400, detail="El id no tiene formato uuid"
        ) from err


class CreatePostRequest(BaseModel):
    routeId: str
    expireAt: datetime
    userId: str


class CreatePostResponse(BaseModel):
    id: str
    userId: str
    createdAt: datetime


class PostResponse(BaseModel):
    id: str
    routeId: str
    userId: str
    expireAt: datetime
    createdAt: datetime


class DeletePostResponse(BaseModel):
    msg: str


class CountResponse(BaseModel):
    count: int


class ResetResponse(BaseModel):
    msg: str


@router.post("", response_model=CreatePostResponse, status_code=201)
def create_post(
    payload: CreatePostRequest,
    use_case: BaseUseCase = Depends(build_create_post_use_case),
):
    """Crea una nueva publicación."""
    post = use_case.execute(
        routeId=payload.routeId,
        userId=payload.userId,
        expireAt=payload.expireAt,
    )
    return CreatePostResponse(id=post.id, userId=post.userId, createdAt=post.createdAt)


@router.get("", response_model=list[PostResponse])
def list_posts(
    expire: bool | None = Query(default=None),
    route: str | None = Query(default=None),
    owner: str | None = Query(default=None),
    use_case: BaseUseCase = Depends(build_list_posts_use_case),
):
    """Ve y filtra publicaciones (todos los filtros son opcionales, AND)."""
    posts = use_case.execute(expire=expire, route=route, owner=owner)
    return [
        PostResponse(
            id=post.id,
            routeId=post.routeId,
            userId=post.userId,
            expireAt=post.expireAt,
            createdAt=post.createdAt,
        )
        for post in posts
    ]


@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"


@router.get("/count", response_model=CountResponse)
def count_posts(use_case: BaseUseCase = Depends(build_count_posts_use_case)):
    """Cuenta cuántas publicaciones hay almacenadas."""
    return CountResponse(count=use_case.execute())


@router.post("/reset", response_model=ResetResponse)
def reset_posts(use_case: BaseUseCase = Depends(build_reset_posts_use_case)):
    """Elimina todas las publicaciones."""
    use_case.execute()
    return ResetResponse(msg="Todos los datos fueron eliminados")


# Las rutas con {post_id} van al final a propósito: si quedaran antes de
# /ping, /count o /reset, esos nombres se interpretarían como un post_id y
# nunca llegarían a su endpoint real.
@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: str,
    use_case: BaseUseCase = Depends(build_get_post_use_case),
):
    """Consulta una publicación por id."""
    _validate_uuid_format(post_id)
    try:
        post = use_case.execute(post_id=post_id)
    except PostNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    return PostResponse(
        id=post.id,
        routeId=post.routeId,
        userId=post.userId,
        expireAt=post.expireAt,
        createdAt=post.createdAt,
    )


@router.delete("/{post_id}", response_model=DeletePostResponse)
def delete_post(
    post_id: str,
    use_case: BaseUseCase = Depends(build_delete_post_use_case),
):
    """Elimina una publicación por id."""
    _validate_uuid_format(post_id)
    try:
        use_case.execute(post_id=post_id)
    except PostNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    return DeletePostResponse(msg="la publicación fue eliminada")
