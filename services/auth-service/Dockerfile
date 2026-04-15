FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Install shared library (build context = project root)
COPY shared /tmp/shared
RUN pip install /tmp/shared && rm -rf /tmp/shared

# Install auth service dependencies
COPY services/auth-service/pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application
COPY services/auth-service/ .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8001/health/ || exit 1

# Run both HTTP and gRPC servers via uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "1"]
