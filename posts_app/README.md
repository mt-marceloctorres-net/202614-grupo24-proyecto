# Posts App

Microservicio de gestión de publicaciones del proyecto **Cargo tu encargo**. Construido en Python 3.11 + FastAPI, con arquitectura hexagonal (dominio / puertos / adaptadores / entrypoints) y PostgreSQL como base de datos, siguiendo el patrón de `users_app/`.

**Estado**: scaffold (tarjeta #23). Los endpoints de negocio (creación/consulta/eliminación de publicaciones) y los técnicos `/posts/count` y `/posts/reset` se agregan en la tarjeta #24, junto con el contrato de API confirmado. Por ahora solo expone `GET /posts/ping`.

## Estructura

```
posts_app/
├── Dockerfile              # Build multi-stage, rootless
├── pyproject.toml          # Dependencias (Poetry)
├── src/
│   ├── config.py           # Configuración por variables de ambiente (pydantic-settings)
│   ├── assembly.py         # Wiring del repositorio (casos de uso llegan en #24)
│   ├── errors.py           # Excepciones de dominio
│   ├── domain/
│   │   ├── models/         # Entidad Publicación (Pydantic)
│   │   ├── ports/          # Interfaz PostRepositoryPort
│   │   └── use_cases/      # Se completa en #24
│   ├── adapters/
│   │   └── postgres/       # Implementación real del puerto (SQLAlchemy)
│   └── entrypoints/
│       └── api/            # Router de FastAPI
└── tests/
    └── unit/                # Pruebas de config y modelo de dominio
```

## Ejecución

### Local, con Poetry

```bash
poetry install
PYTHONPATH=$(pwd)/src poetry run uvicorn entrypoints.api.main:app --host 0.0.0.0 --port 9000
```

El API queda disponible en `http://localhost:9000`. Documentación interactiva en `http://localhost:9000/docs`.

### Variables de ambiente

| Variable | Default | Descripción |
|---|---|---|
| `APP_NAME` | `Posts app` | Nombre de la aplicación |
| `LOG_LEVEL` | `DEBUG` | Nivel de logging |
| `DB_HOST` | `localhost` | Host de Postgres |
| `DB_PORT` | `5432` | Puerto de Postgres |
| `DB_NAME` | `posts_db` | Nombre de la base de datos |
| `DB_USER` | `postgres` | Usuario de la base de datos |
| `DB_PASSWORD` | `postgres` | Contraseña de la base de datos |

`posts_app` no maneja sesiones, por lo que no tiene `TOKEN_EXPIRATION_MINUTES` (esa variable es exclusiva de `users_app`).

### Con Docker

```bash
docker build --rm -t posts_app:v1.0.0 -f Dockerfile --target runner --label version=v1.0.0 .
docker run -p 9000:9000 \
  -e DB_HOST=<host> -e DB_PORT=5432 -e DB_NAME=posts_db -e DB_USER=postgres -e DB_PASSWORD=postgres \
  posts_app:v1.0.0
```

`<host>` es el nombre del servicio de Postgres en tu `docker-compose.yml`/red de Docker, o el Service `posts-db-service` en Kubernetes — nunca `localhost` fijo.

## Pruebas

```bash
poetry install
poetry run pytest --cov=src -v -s --cov-report term-missing
```

## Autor

Marco Torres — [mar-torr@uniandes.edu.co](mailto:mar-torr@uniandes.edu.co)
