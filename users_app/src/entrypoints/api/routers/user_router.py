from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from assembly import build_create_user_use_case, build_update_user_use_case
from domain.models.user import UserStatus
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidRequestError, UserAlreadyExistsError, UserNotFoundError

# Los endpoints de autenticación (/auth, /me) y técnicos (/count, /ping,
# /reset) se agregan en los issues #11 y #12.
router = APIRouter(prefix="/users")


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
