from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseORM(DeclarativeBase):
    """Declarative base for PostgreSQL models."""


class RouteORM(BaseORM):
    """ORM model for route entity."""

    __tablename__ = "routes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    flight_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    source_airport_code: Mapped[str] = mapped_column(String(10), nullable=False)
    source_country: Mapped[str] = mapped_column(String(100), nullable=False)
    destiny_airport_code: Mapped[str] = mapped_column(String(10), nullable=False)
    destiny_country: Mapped[str] = mapped_column(String(100), nullable=False)
    bag_cost: Mapped[float] = mapped_column(Float, nullable=False)
    planned_start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )
    planned_end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


__all__ = ["BaseORM", "RouteORM"]
