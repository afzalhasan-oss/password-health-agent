from typing import Literal


def compute_score(password_count: int, oldest_password_age_days: int) -> int:
    """Computes a deterministic health score from password count and max password age."""

    age_penalty = min(oldest_password_age_days // 30, 60)
    count_penalty = 0
    if password_count < 5:
        count_penalty = 30
    elif password_count < 15:
        count_penalty = 15
    elif password_count < 30:
        count_penalty = 5

    score = 100 - age_penalty - count_penalty
    return max(0, min(100, score))


def get_status(score: int) -> Literal["HEALTHY", "OKAY", "CRITICAL"]:
    """Maps a score to the agreed fixed status bands."""

    if score >= 75:
        return "HEALTHY"
    if score >= 40:
        return "OKAY"
    return "CRITICAL"


def get_color(status: Literal["HEALTHY", "OKAY", "CRITICAL"]) -> Literal["green", "yellow", "red"]:
    """Maps a status value to the UI color token used by the frontend."""

    mapping = {
        "HEALTHY": "green",
        "OKAY": "yellow",
        "CRITICAL": "red",
    }
    return mapping[status]
