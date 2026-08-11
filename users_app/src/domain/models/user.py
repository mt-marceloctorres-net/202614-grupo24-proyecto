from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserStatus(str, Enum):
    """Estado de un usuario."""

    POR_VERIFICAR = "POR_VERIFICAR"
    NO_VERIFICADO = "NO_VERIFICADO"
    VERIFICADO = "VERIFICADO"


class User(BaseModel):
    """Modelo de dominio Usuario."""

    id: str | None = None
    username: str = Field(min_length=1, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    phoneNumber: str | None = None
    dni: str | None = None
    fullName: str | None = None
    password: str
    salt: str | None = None
    token: str | None = None
    status: UserStatus = UserStatus.POR_VERIFICAR
    expireAt: datetime | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
