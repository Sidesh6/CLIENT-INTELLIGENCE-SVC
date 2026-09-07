from datetime import UTC, datetime
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str = "client-intelligence-svc"
    version: str = "0.1.0"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


@router.get("/health", response_model=HealthResponse)
@router.get("/api/v1/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """Check service health."""
    return HealthResponse()
