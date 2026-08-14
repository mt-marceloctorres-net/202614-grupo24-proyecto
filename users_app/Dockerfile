FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.1.1

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --only main --no-interaction --no-ansi

COPY src ./src

FROM python:3.11-slim AS runner

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app app

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

USER app

EXPOSE 9000

CMD ["uvicorn", "entrypoints.api.main:app", "--host", "0.0.0.0", "--port", "9000"]
