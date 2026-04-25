from fastapi import HTTPException


def validate_input_ranges(password_count: int, oldest_password_age_days: int) -> None:
    """Applies additional domain-level validation with friendly guidance on constraints."""

    if password_count < 0 or oldest_password_age_days < 0:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_RANGE",
                "message": "Values cannot be negative. Please enter non-negative numbers.",
                "details": [],
            },
        )
