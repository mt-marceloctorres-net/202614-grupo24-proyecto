from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Trayecto(BaseModel):
    """Domain model for a route/trayecto."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    id: str | None = None
    flightId: str = Field(..., min_length=1)
    sourceAirportCode: str = Field(..., min_length=1)
    sourceCountry: str = Field(..., min_length=1)
    destinyAirportCode: str = Field(..., min_length=1)
    destinyCountry: str = Field(..., min_length=1)
    bagCost: float = Field(..., gt=0)
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


Route = Trayecto

__all__ = ["Route", "Trayecto"]
