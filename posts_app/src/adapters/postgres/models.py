from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa de SQLAlchemy."""

    pass


def utcnow() -> datetime:
    """Fecha y hora actual en UTC, sin tzinfo (formato ISO yyyy-mm-ddTHH:MM:SS)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class PostModel(Base):
    """Tabla de publicaciones."""

    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    routeId: Mapped[str] = mapped_column(String, nullable=False)
    userId: Mapped[str] = mapped_column(String, nullable=False)
    expireAt: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, nullable=False
    )
