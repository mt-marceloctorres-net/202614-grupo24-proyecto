# Routes App

Aplicación base para la capa de trayectos siguiendo una arquitectura hexagonal con FastAPI y PostgreSQL.

## Estructura

- src/config.py: configuración y conexión a la base de datos
- src/assembly.py: ensamblaje de dependencias
- src/domain/: modelos, puertos y casos de uso
- src/adapters/postgres/: adaptador SQLAlchemy para PostgreSQL
- src/entrypoints/api/: FastAPI app y routers

## Variables de entorno

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD
- APP_NAME
- LOG_LEVEL

## Ejecución local

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=routes_db
export DB_USER=postgres
export DB_PASSWORD=postgres

python -m uvicorn src.entrypoints.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker build -t routes_app:local .
docker run --rm -p 8000:8000 --network host routes_app:local
```
