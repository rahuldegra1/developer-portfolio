from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.logging_config import logger
from app.middleware import ObservabilityMiddleware
from app.routers import leads

app = FastAPI(
    title="Lead Ingestion Service",
    version="1.0.0",
    description="Microservice for validating, storing, and filtering inbound sales leads.",
)

# Register custom observability middleware
app.add_middleware(ObservabilityMiddleware)

# Include endpoint router
app.include_router(leads.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        f"Unhandled application error: {str(exc)}",
        exc_info=True,
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error. Please reference the request ID when contacting support.",
            "request_id": request_id,
        },
        headers={"X-Request-ID": request_id},
    )


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "lead-ingestion"}
