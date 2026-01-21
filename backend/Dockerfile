FROM python:3.12-bullseye

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install system deps including curl
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*


# Python deps
COPY pyproject.toml uv.lock /app/

RUN uv sync --no-dev --no-cache

COPY src/ /app/

EXPOSE 8000

CMD ["uv", "run", "--no-dev", "uvicorn", "app:app", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]