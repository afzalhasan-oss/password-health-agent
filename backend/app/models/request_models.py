from pydantic import BaseModel, Field


class HealthCheckRequest(BaseModel):
    """Represents the user input payload for a password health check."""

    passwordCount: int = Field(ge=0, le=1_000_000)
    oldestPasswordAgeDays: int = Field(ge=0, le=36_500)
