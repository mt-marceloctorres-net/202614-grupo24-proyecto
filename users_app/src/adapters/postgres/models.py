from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa de SQLAlchemy."""

    pass


def utcnow() -> datetime:
    """Fecha y hora actual en UTC, sin tzinfo (formato ISO yyyy-mm-ddTHH:MM:SS)."""
    return datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)


class UserModel(Base):
    """Tabla de usuarios."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phoneNumber: Mapped[str | None] = mapped_column(String, nullable=True)
    dni: Mapped[str | None] = mapped_column(String, nullable=True)
    fullName: Mapped[str | None] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    salt: Mapped[str | None] = mapped_column(String, nullable=True)
    token: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="POR_VERIFICAR")
    expireAt: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, nullable=False
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, onupdate=utcnow, nullable=False
    )
