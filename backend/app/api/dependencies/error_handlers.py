from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def install_error_handlers(app: FastAPI) -> None:
    """Registers global exception handlers that return friendly structured JSON errors."""

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Converts request validation failures into consistent client-facing messages."""

        details = []
        for error in exc.errors():
            location = ".".join([str(item) for item in error.get("loc", []) if item != "body"])
            message = error.get("msg", "Invalid input")
            details.append(f"{location}: {message}" if location else message)

        return JSONResponse(
            status_code=400,
            content={
                "code": "VALIDATION_ERROR",
                "message": "Please check your input and try again.",
                "details": details,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        """Returns a safe generic message for unexpected server errors."""

        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_ERROR",
                "message": "Something went wrong on our side. Please try again in a moment.",
                "details": [],
            },
        )
