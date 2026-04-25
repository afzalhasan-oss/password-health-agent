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


# Configures CORS for frontend calls that include session cookies.
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
