import json
import os
from pathlib import Path
from typing import Any

from jsonschema import ValidationError, validate
from app.models.response_models import GuidanceItemResponse


def _schema() -> dict[str, Any]:
    """Loads the JSON schema used to validate structured agent responses."""

    schema_path = Path(__file__).resolve().parents[3] / "specs" / "001-password-health-chat" / "contracts" / "agent-response.schema.json"
    with schema_path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def _to_guidance_items(payload: dict[str, Any]) -> list[GuidanceItemResponse]:
    """Maps validated agent payload objects into response model instances."""

    return [
        GuidanceItemResponse(
            priorityRank=item["priorityRank"],
            title=item["title"],
            detail=item["detail"],
        )
        for item in payload.get("guidance", [])
    ]


async def generate_guidance(
    password_count: int,
    oldest_password_age_days: int,
    score: int,
    status: str,
) -> list[GuidanceItemResponse]:
    """Generates schema-validated guidance from OpenAI Agent SDK or returns empty on failure."""

    try:
        from agents import Agent, Runner  # type: ignore
    except Exception:
        return []

    prompt = (
        "You are a helpful security coach. Return only structured JSON with keys score, status, guidance. "
        "Guidance must be prioritized, concise, encouraging, and non-scary. "
        "Input: "
        f"password_count={password_count}, oldest_password_age_days={oldest_password_age_days}, score={score}, status={status}."
    )

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    agent = Agent(
        name="password_health_agent",
        instructions="Return valid JSON only.",
        model=model_name,
    )

    try:
        result = await Runner.run(agent, prompt)
        text_output = str(result.final_output)
        parsed = json.loads(text_output)
        validate(instance=parsed, schema=_schema())
        return _to_guidance_items(parsed)
    except (ValidationError, json.JSONDecodeError, Exception):
        return []
