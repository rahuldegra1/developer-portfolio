from fastapi import FastAPI

from app.routers.leads import router as leads_router


# Ensure tables are built
# Base.metadata.create_all(bind=engine)
def test_observability_middleware_headers(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time" in response.headers
    assert response.headers["X-Process-Time"].endswith("ms")


app = FastAPI(
    title="Production Lead Ingestion Microservice",
    description="Modular clean architecture with FastAPI, Pydantic v2, and SQLAlchemy.",
    version="1.0.0",
)

app.include_router(leads_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "lead-ingestion"}
