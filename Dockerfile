# Multi-stage Dockerfile for TCM Application

# Stage 1: Builder
FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy uv from builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ /app/src/
COPY pyproject.toml ./

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=2)" || exit 1

# Run the application
CMD ["uvicorn", "tcm.main:app", "--host", "0.0.0.0", "--port", "8000"]
