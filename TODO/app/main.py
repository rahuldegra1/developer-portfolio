from fastapi import FastAPI
from app.middleware import ObservabilityMiddleware
from app.routers import leads

app = FastAPI(
    title="Lead Ingestion Service",
    version="1.0.0",
    description="Microservice for validating, storing, and filtering inbound sales leads.",
)

# Register custom observability middleware
app.add_middleware(ObservabilityMiddleware)

# Include endpoint router (prefix="/leads" is already defined in leads.py)
app.include_router(leads.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "lead-ingestion"}
