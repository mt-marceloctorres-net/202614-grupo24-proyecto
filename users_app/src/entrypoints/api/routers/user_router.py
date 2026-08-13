from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field

from assembly import (
    build_authenticate_user_use_case,
    build_count_users_use_case,
    build_create_user_use_case,
    build_get_me_use_case,
    build_reset_users_use_case,
    build_update_user_use_case,
)
from domain.models.user import UserStatus
from domain.use_cases.base_use_case import BaseUseCase
from errors import (
    InvalidCredentialsError,
    InvalidRequestError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

# Los endpoints técnicos (/count, /ping, /reset) se agregan en el issue #12.
router = APIRouter(prefix="/users")
bearer_scheme = HTTPBearer()


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=1, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=1)
    email: EmailStr
    dni: str | None = None
    fullName: str | None = None
    phoneNumber: str | None = None


class CreateUserResponse(BaseModel):
    id: str
    createdAt: datetime


class UpdateUserRequest(BaseModel):
    status: UserStatus | None = None
    dni: str | None = None
    fullName: str | None = None
    phoneNumber: str | None = None


class UpdateUserResponse(BaseModel):
    msg: str


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    id: str
    token: str
    expireAt: datetime


class CountResponse(BaseModel):
    count: int


class ResetResponse(BaseModel):
    msg: str


class MeResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    fullName: str | None = None
    dni: str | None = None
    phoneNumber: str | None = None
    status: UserStatus


@router.post("", response_model=CreateUserResponse, status_code=201)
def create_user(
    payload: CreateUserRequest,
    use_case: BaseUseCase = Depends(build_create_user_use_case),
):
    """Crea un nuevo usuario."""
    try:
        user = use_case.execute(
            username=payload.username,
            password=payload.password,
            email=payload.email,
            dni=payload.dni,
            fullName=payload.fullName,
            phoneNumber=payload.phoneNumber,
        )
    except UserAlreadyExistsError as err:
        raise HTTPException(status_code=412, detail=str(err)) from err
    return CreateUserResponse(id=user.id, createdAt=user.createdAt)


@router.patch("/{user_id}", response_model=UpdateUserResponse)
def update_user(
    user_id: str,
    payload: UpdateUserRequest,
    use_case: BaseUseCase = Depends(build_update_user_use_case),
):
    """Actualiza los datos públicos de un usuario."""
    try:
        use_case.execute(
            user_id=user_id,
            status=payload.status,
            dni=payload.dni,
            fullName=payload.fullName,
            phoneNumber=payload.phoneNumber,
        )
    except InvalidRequestError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except UserNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    return UpdateUserResponse(msg="el usuario ha sido actualizado")


@router.post("/auth", response_model=AuthResponse)
def authenticate_user(
    payload: AuthRequest,
    use_case: BaseUseCase = Depends(build_authenticate_user_use_case),
):
    """Genera un nuevo token de sesión para el usuario."""
    try:
        user = use_case.execute(username=payload.username, password=payload.password)
    except InvalidCredentialsError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    return AuthResponse(id=user.id, token=user.token, expireAt=user.expireAt)


@router.get("/me", response_model=MeResponse)
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    use_case: BaseUseCase = Depends(build_get_me_use_case),
):
    """Retorna los datos del usuario dueño del token."""
    try:
        user = use_case.execute(token=credentials.credentials)
    except InvalidTokenError as err:
        raise HTTPException(status_code=401, detail=str(err)) from err
    return MeResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        fullName=user.fullName,
        dni=user.dni,
        phoneNumber=user.phoneNumber,
        status=user.status,
    )


@router.get("/count", response_model=CountResponse)
def count_users(use_case: BaseUseCase = Depends(build_count_users_use_case)):
    """Cuenta cuántos usuarios hay almacenados."""
    return CountResponse(count=use_case.execute())


@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"


@router.post("/reset", response_model=ResetResponse)
def reset_users(use_case: BaseUseCase = Depends(build_reset_users_use_case)):
    """Elimina todos los usuarios."""
    use_case.execute()
    return ResetResponse(msg="Todos los datos fueron eliminados")
