from app.agents.password_health_agent import generate_guidance
from app.models.response_models import GuidanceItemResponse


def fallback_guidance(status: str) -> list[GuidanceItemResponse]:
    """Builds safe default guidance entries when agent output is unavailable."""

    if status == "CRITICAL":
        messages = [
            (1, "Update oldest passwords first", "Start with your oldest passwords and replace them with new unique ones."),
            (2, "Increase password variety", "Add more distinct passwords so important accounts are not reused."),
            (3, "Keep momentum", "Small weekly improvements will raise your score quickly."),
        ]
    elif status == "OKAY":
        messages = [
            (1, "Refresh aging passwords", "Rotate passwords that have not changed in a long time."),
            (2, "Boost unique coverage", "Aim for unique passwords on your highest-value accounts first."),
            (3, "You are on track", "A few updates can move you into the Healthy range."),
        ]
    else:
        messages = [
            (1, "Maintain your routine", "Keep rotating old passwords on a regular schedule."),
            (2, "Prioritize critical accounts", "Review email, banking, and cloud credentials first."),
            (3, "Great progress", "You are doing well; consistency keeps your score strong."),
        ]
    return [GuidanceItemResponse(priorityRank=p, title=t, detail=d) for p, t, d in messages]


async def get_recommendations(
    password_count: int,
    oldest_password_age_days: int,
    score: int,
    status: str,
) -> list[GuidanceItemResponse]:
    """Returns validated guidance from agent output with graceful fallback on errors."""

    guidance = await generate_guidance(
        password_count=password_count,
        oldest_password_age_days=oldest_password_age_days,
        score=score,
        status=status,
    )
    if guidance:
        return guidance
    return fallback_guidance(status)
