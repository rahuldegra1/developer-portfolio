# -------------------------------------------------------------
# Stage 1: Build & Wheel Compilation
# -------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a self-contained virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------------------
# Stage 2: Hardened Non-Root Runtime
# -------------------------------------------------------------
FROM python:3.12-slim AS runtime

WORKDIR /app

# Create unprivileged system group and user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10000 -g appgroup -s /sbin/nologin -d /app appuser

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Ensure PATH prioritizes the virtual environment binaries (uvicorn, alembic)
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy project files and assign ownership to appuser
COPY --chown=appuser:appgroup alembic.ini ./
COPY --chown=appuser:appgroup alembic/ ./alembic/
COPY --chown=appuser:appgroup app/ ./app/

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]