# Imagen base delgada: trae Python 3.11 sin las herramientas de compilación que
# no necesitamos, porque psycopg2-binary ya viene compilado.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.3 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

# Las dependencias se copian e instalan antes que el código: mientras
# pyproject.toml y poetry.lock no cambien, Docker reutiliza esta capa y no
# vuelve a descargar todo en cada build.
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction --no-ansi

COPY src/ ./src/

# Los módulos se importan sin el prefijo `src.` (por ejemplo `from config import
# settings`), igual que en las pruebas. Por eso `src` va en el PYTHONPATH en vez
# de tratarse como paquete.
ENV PYTHONPATH=/app/src

EXPOSE 3000

CMD ["uvicorn", "entrypoints.api.main:app", "--host", "0.0.0.0", "--port", "3000"]
