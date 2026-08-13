from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa de SQLAlchemy."""

    pass


def utcnow() -> datetime:
    """Fecha y hora actual en UTC, sin tzinfo (formato ISO yyyy-mm-ddTHH:MM:SS)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class OfferModel(Base):
    """Tabla de ofertas."""

    __tablename__ = "offers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    postId: Mapped[str] = mapped_column(String, nullable=False, index=True)
    userId: Mapped[str] = mapped_column(String, nullable=False, index=True)
    # El límite de 140 viene de `information.md`. La validación real ocurre en el
    # dominio, que devuelve un error de contrato; esta longitud está aquí para
    # que el esquema de la base refleje el modelo de datos documentado y como
    # última barrera si algún día se escribe por fuera del caso de uso.
    description: Mapped[str] = mapped_column(String(140), nullable=False)
    size: Mapped[str] = mapped_column(String, nullable=False)
    fragile: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    offer: Mapped[float] = mapped_column(Float, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, nullable=False
    )
