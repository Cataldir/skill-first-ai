# syntax=docker/dockerfile:1.7
#
# linux/amd64 image for the MCP server. Used for either Path A
# (Container Apps behind APIM) or Path B (Foundry Hosted Agent).

FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install uv for fast, reproducible resolution.
RUN pip install uv

COPY pyproject.toml README.md ./
COPY src ./src

RUN uv pip install --system --no-cache .

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY src ./src
COPY pyproject.toml README.md ./

EXPOSE 8080

# Non-root for ACR + Container Apps best practice.
RUN useradd --create-home --uid 10001 app
USER app

CMD ["uvicorn", "skill_first_ai.foundry.mcp_server:app", "--host", "0.0.0.0", "--port", "8080"]
