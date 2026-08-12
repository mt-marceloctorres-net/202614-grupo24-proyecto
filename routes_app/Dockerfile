FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=local \
    DB_HOST=localhost \
    DB_PORT=5432 \
    DB_NAME=routes_db \
    DB_USER=postgres \
    DB_PASSWORD=postgres

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --with dev || true

COPY src ./src

EXPOSE 8000

CMD ["uvicorn", "src.entrypoints.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
