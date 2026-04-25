import logging

from fastapi import APIRouter, Request, Response

from app.api.dependencies.validation import validate_input_ranges
from app.db.prisma_client import prisma_facade
from app.db.session_store import get_or_create_session_hash
from app.models.request_models import HealthCheckRequest
from app.models.response_models import HealthCheckResponse, HistoryItemResponse, HistoryResponse, TrendResponse
from app.services.history_service import compute_trend, get_history, save_assessment
from app.services.recommendation_service import get_recommendations
from app.services.scoring_service import compute_score, get_color, get_status

router = APIRouter(prefix="/v1/health-checks", tags=["health-checks"])
logger = logging.getLogger("password_health_api.routes.health_checks")


@router.post("", response_model=HealthCheckResponse)
async def create_health_check(payload: HealthCheckRequest, request: Request, response: Response) -> HealthCheckResponse:
    """Creates a new password health assessment and returns score, status, color, and guidance."""

    logger.info("create_health_check.started")
    validate_input_ranges(payload.passwordCount, payload.oldestPasswordAgeDays)
    session_hash = get_or_create_session_hash(request, response)

    score = compute_score(payload.passwordCount, payload.oldestPasswordAgeDays)
    status = get_status(score)
    color = get_color(status)

    guidance = await get_recommendations(
        password_count=payload.passwordCount,
        oldest_password_age_days=payload.oldestPasswordAgeDays,
        score=score,
        status=status,
    )

    entry = await save_assessment(
        session_hash=session_hash,
        password_count=payload.passwordCount,
        oldest_age_days=payload.oldestPasswordAgeDays,
        score=score,
        status=status,
        color=color,
        guidance=guidance,
        prisma_client=prisma_facade.client,
    )

    logger.info("create_health_check.completed status=%s score=%s", status, score)

    return HealthCheckResponse(
        assessmentId=entry["assessmentId"],
        score=score,
        status=status,
        color=color,
        guidance=guidance,
    )


@router.get("/history", response_model=HistoryResponse)
async def get_health_check_history(request: Request, response: Response) -> HistoryResponse:
    """Returns chronological assessment history and trend metadata for current session."""

    logger.info("get_health_check_history.started")
    session_hash = get_or_create_session_hash(request, response)
    history = await get_history(session_hash, prisma_client=prisma_facade.client)

    items = [
        HistoryItemResponse(
            assessmentId=item["assessmentId"],
            score=item["score"],
            status=item["status"],
            createdAt=item["createdAt"],
        )
        for item in history
    ]

    trend = compute_trend(history)
    logger.info("get_health_check_history.completed items=%s", len(items))
    return HistoryResponse(
        items=items,
        trend=TrendResponse(**trend),
    )
