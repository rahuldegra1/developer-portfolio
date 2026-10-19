from fastapi import FastAPI

from app.routers.leads import router as leads_router

# Ensure tables are built
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Production Lead Ingestion Microservice",
    description="Modular clean architecture with FastAPI, Pydantic v2, and SQLAlchemy.",
    version="1.0.0",
)

app.include_router(leads_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "lead-ingestion"}
