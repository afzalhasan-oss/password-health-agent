from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.models.response_models import GuidanceItemResponse


_MEMORY_DB: dict[str, list[dict[str, Any]]] = {}


async def save_assessment(
    session_hash: str,
    password_count: int,
    oldest_age_days: int,
    score: int,
    status: str,
    color: str,
    guidance: list[GuidanceItemResponse],
    prisma_client: Any = None,
) -> dict[str, Any]:
    """Persists an assessment and guidance items using Prisma when available or memory fallback."""

    assessment_id = str(uuid4())
    created_at = datetime.now(timezone.utc)
    entry = {
        "assessmentId": assessment_id,
        "passwordCount": password_count,
        "oldestPasswordAgeDays": oldest_age_days,
        "score": score,
        "status": status,
        "color": color,
        "createdAt": created_at,
        "guidance": [item.model_dump() for item in guidance],
    }

    if prisma_client is not None:
        try:
            session = await prisma_client.sessioncontext.upsert(
                where={"sessionTokenHash": session_hash},
                data={
                    "create": {"sessionTokenHash": session_hash},
                    "update": {},
                },
            )
            assessment = await prisma_client.healthassessment.create(
                data={
                    "id": assessment_id,
                    "sessionContextId": session.id,
                    "passwordCount": password_count,
                    "oldestPasswordAgeDays": oldest_age_days,
                    "score": score,
                    "status": status,
                    "agentModel": "gpt-4o-mini",
                }
            )
            for item in guidance:
                await prisma_client.guidanceitem.create(
                    data={
                        "assessmentId": assessment.id,
                        "priorityRank": item.priorityRank,
                        "title": item.title,
                        "detail": item.detail,
                    }
                )
            entry["createdAt"] = assessment.createdAt
        except Exception:
            pass

    if session_hash not in _MEMORY_DB:
        _MEMORY_DB[session_hash] = []
    _MEMORY_DB[session_hash].append(entry)
    return entry


async def get_history(session_hash: str, prisma_client: Any = None) -> list[dict[str, Any]]:
    """Returns chronologically sorted history entries for the current session identity."""

    if prisma_client is not None:
        try:
            session = await prisma_client.sessioncontext.find_unique(
                where={"sessionTokenHash": session_hash}
            )
            if session is not None:
                assessments = await prisma_client.healthassessment.find_many(
                    where={"sessionContextId": session.id},
                    order={"createdAt": "asc"},
                    include={"guidanceItems": True},
                )
                mapped: list[dict[str, Any]] = []
                for assessment in assessments:
                    mapped.append(
                        {
                            "assessmentId": assessment.id,
                            "score": assessment.score,
                            "status": assessment.status,
                            "createdAt": assessment.createdAt,
                        }
                    )
                return mapped
        except Exception:
            pass

    return sorted(_MEMORY_DB.get(session_hash, []), key=lambda x: x["createdAt"])


def compute_trend(history: list[dict[str, Any]]) -> dict[str, Any]:
    """Computes trend direction and score delta from the latest two history entries."""

    if len(history) < 2:
        return {"direction": "STABLE", "deltaFromPrevious": 0}

    previous = history[-2]["score"]
    latest = history[-1]["score"]
    delta = latest - previous
    if delta > 0:
        direction = "IMPROVING"
    elif delta < 0:
        direction = "DECLINING"
    else:
        direction = "STABLE"
    return {"direction": direction, "deltaFromPrevious": delta}
