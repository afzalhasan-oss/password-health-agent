import hashlib
import hmac
import os
import secrets
from fastapi import Request, Response

COOKIE_NAME = "ph_session"


def _secret() -> bytes:
    """Loads the configured cookie signing secret from environment variables."""

    return os.getenv("SESSION_COOKIE_SECRET", "dev-only-secret-change-me").encode("utf-8")


def _sign(raw_value: str) -> str:
    """Signs a session token value with HMAC so tampering can be detected."""

    digest = hmac.new(_secret(), raw_value.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{raw_value}.{digest}"


def _verify(signed_value: str) -> str | None:
    """Verifies a signed session token and returns the raw token when valid."""

    if "." not in signed_value:
        return None
    raw, provided_sig = signed_value.split(".", 1)
    expected = hmac.new(_secret(), raw.encode("utf-8"), hashlib.sha256).hexdigest()
    if hmac.compare_digest(expected, provided_sig):
        return raw
    return None


def token_hash(raw_value: str) -> str:
    """Returns a hashed token representation suitable for database storage."""

    return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()


def get_or_create_session_hash(request: Request, response: Response) -> str:
    """Gets or creates a signed session cookie and returns its hashed identity key."""

    signed = request.cookies.get(COOKIE_NAME)
    raw = _verify(signed) if signed else None
    if raw is None:
        raw = secrets.token_urlsafe(32)
        signed = _sign(raw)
        cookie_secure = os.getenv("COOKIE_SECURE", "false").lower() == "true"
        cookie_domain = os.getenv("COOKIE_DOMAIN")
        response.set_cookie(
            key=COOKIE_NAME,
            value=signed,
            httponly=True,
            secure=cookie_secure,
            samesite="lax",
            max_age=60 * 60 * 24 * 365,
            domain=cookie_domain,
        )
    return token_hash(raw)
