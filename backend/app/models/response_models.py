from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


StatusType = Literal["HEALTHY", "OKAY", "CRITICAL"]
TrendDirection = Literal["IMPROVING", "STABLE", "DECLINING"]


class GuidanceItemResponse(BaseModel):
    """Represents a single prioritized recommendation item for the user."""

    priorityRank: int = Field(ge=1)
    title: str
    detail: str


class HealthCheckResponse(BaseModel):
    """Represents the API response for a created health assessment."""

    assessmentId: str
    score: int = Field(ge=0, le=100)
    status: StatusType
    color: Literal["green", "yellow", "red"]
    guidance: list[GuidanceItemResponse]


class HistoryItemResponse(BaseModel):
    """Represents one historical health assessment entry for the session."""

    assessmentId: str
    score: int = Field(ge=0, le=100)
    status: StatusType
    createdAt: datetime


class TrendResponse(BaseModel):
    """Represents trend metadata derived from historical scores."""

    direction: TrendDirection
    deltaFromPrevious: int


class HistoryResponse(BaseModel):
    """Represents the API response containing history entries and trend info."""

    items: list[HistoryItemResponse]
    trend: TrendResponse


class ErrorResponse(BaseModel):
    """Represents the standard API error shape returned to the frontend."""

    code: str
    message: str
    details: list[str] = []
