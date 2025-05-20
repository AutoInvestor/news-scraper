########################  Builder  ########################
FROM python:3.11 AS builder

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH" \
    PYTHONPATH="/app/src"

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main --no-root && \
    rm -rf ~/.cache/pypoetry ~/.cache/pip

########################  Runtime  ########################
FROM python:3.11-slim

# install the OpenMP runtime that LightGBM needs
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 PYTHONPATH="/app/src"

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages \
                     /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src ./src

# Kubernetes will override these with the real secrets via env.
ENV GCP_PROJECT="" \
    PUBSUB_TOPIC="" \
    MONGODB_URI="" \
    MONGODB_DB=""

EXPOSE 8080
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
