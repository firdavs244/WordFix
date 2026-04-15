FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install shared library (build context = project root)
COPY shared /tmp/shared
RUN pip install /tmp/shared && rm -rf /tmp/shared

# Install gateway dependencies
COPY services/api-gateway/pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application
COPY services/api-gateway/ .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8080/api/v1/health/ || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
