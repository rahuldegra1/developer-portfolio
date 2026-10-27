# Use a slim Python 3.12 base image
FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies in a single cached layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model checkpoint and API code
COPY resnet18_cifar10.pth .
COPY api.py .

# Expose FastAPI's default port
EXPOSE 8000

# Start Uvicorn bound to all interfaces
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]