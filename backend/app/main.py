import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dependencies.error_handlers import install_error_handlers
from app.api.routes.health_checks import router as health_checks_router
from app.db.prisma_client import prisma_facade

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("password_health_api")

app = FastAPI(title="Password Health Checker API", version="0.1.0")


def _allowed_origins() -> list[str]:
    """Builds CORS allow-list from environment with safe local default."""
    origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
    return [origin]


def _configure_cors(app: FastAPI) -> None:
    """Configures CORS middleware for frontend calls with session cookies.
    
    When credentials (cookies) are included, wildcards (*) are not allowed for
    origins, methods, or headers. All must be explicitly listed.
    
    The middleware must be added before other middleware to intercept OPTIONS preflight requests.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins(),
        allow_credentials=True,  # Required for session cookies (Set-Cookie headers)
        allow_methods=["GET", "POST", "OPTIONS"],  # Explicit methods (no wildcard with credentials)
        allow_headers=["Content-Type", "Authorization"],  # Explicit headers
        expose_headers=["Content-Type"],  # Headers accessible to frontend JavaScript
        max_age=600,  # Cache preflight response for 10 minutes
    )


# Add CORS middleware FIRST (before other middleware and routes)
_configure_cors(app)

install_error_handlers(app)
app.include_router(health_checks_router)


@app.on_event("startup")
async def on_startup() -> None:
    """Initializes database connectivity during application startup."""

    app_env = os.getenv("APP_ENV", "development").lower()
    cookie_secure = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    if app_env == "production" and not cookie_secure:
        logger.warning("COOKIE_SECURE should be true in production environments.")

    await prisma_facade.connect()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Closes database connectivity during graceful application shutdown."""

    await prisma_facade.disconnect()
