from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from assembly import build_create_post_use_case
from domain.use_cases.base_use_case import BaseUseCase

# Los endpoints técnicos /posts/count y /posts/reset, y los de
# ver/filtrar/consultar/eliminar, se agregan en las tarjetas #25/#26.
router = APIRouter(prefix="/posts")


class CreatePostRequest(BaseModel):
    routeId: str
    expireAt: datetime
    userId: str


class CreatePostResponse(BaseModel):
    id: str
    userId: str
    createdAt: datetime


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


@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"
