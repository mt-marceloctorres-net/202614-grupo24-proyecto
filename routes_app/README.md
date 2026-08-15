# Routes App

Aplicación de gestión de rutas construida con FastAPI, PostgreSQL y arquitectura hexagonal (dominio, puertos, adaptadores y entrypoints).

## Tabla de contenido

- [Routes App](#routes-app)
	- [Tabla de contenido](#tabla-de-contenido)
	- [Estructura del proyecto](#estructura-del-proyecto)
	- [Variables de ambiente](#variables-de-ambiente)
	- [Ejecución local](#ejecución-local)
	- [Ejecución con Docker](#ejecución-con-docker)
	- [API](#api)
	- [Pruebas](#pruebas)
	- [Autores](#autores)

## Estructura del proyecto

```text
.
├── src/
│   ├── domain/
│   │   ├── models/          # Entidades de dominio
│   │   ├── ports/           # Interfaces de repositorio
│   │   └── use_cases/       # Casos de uso
│   ├── adapters/
│   │   └── postgres/        # Implementación SQLAlchemy + PostgreSQL
│   ├── entrypoints/
│   │   └── api/             # FastAPI app y routers
│   ├── assembly.py          # Inyección de dependencias
│   ├── config.py            # Configuración por variables de entorno
│   └── errors.py            # Excepciones de dominio y aplicación
├── tests/                   # Pruebas unitarias
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Variables de ambiente

La aplicación usa estas variables:

- `DB_HOST` (default: `localhost`)
- `DB_PORT` (default: `5432`)
- `DB_NAME` (default: `routes_db`)
- `DB_USER` (default: `postgres`)
- `DB_PASSWORD` (default: `postgres`)
- `APP_NAME` (default: `Routes app`)
- `LOG_LEVEL` (default: `INFO`)

## Ejecución local

Requisitos:

- Python 3.11
- Poetry 2.1.1+
- PostgreSQL

Instalar dependencias:

```bash
poetry install
```

Configurar variables y ejecutar:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=routes_db
export DB_USER=postgres
export DB_PASSWORD=postgres

poetry run uvicorn src.entrypoints.api.main:app --host 0.0.0.0 --port 9000 --reload
```

## Ejecución con Docker

```bash
docker build -t routes_app:v1.0.0 .
docker run --rm -p 9000:9000 \
	-e DB_HOST=host.docker.internal \
	-e DB_PORT=5432 \
	-e DB_NAME=routes_db \
	-e DB_USER=postgres \
	-e DB_PASSWORD=postgres \
	routes_app:v1.0.0
```

## API

Prefijo base: `/routes`

- `GET /routes/ping`: health check. Respuesta `pong`.
- `GET /routes/count`: retorna el total de rutas (`{"count": n}`).
- `POST /routes/reset`: elimina todas las rutas (idempotente).
- `POST /routes`: crea una ruta. Retorna `201` con **solo** `{"id": "...", "createdAt": "..."}` (no la ruta completa).
	- Retorna `412` para `flightId` duplicado o fechas inválidas.
	- Retorna `400` para errores de validación del payload.
- `GET /routes`: lista rutas.
	- Soporta filtro opcional por query param `flight`.
- `GET /routes/{route_id}`: consulta una ruta por UUID.
	- Retorna `404` si no existe.
- `DELETE /routes/{route_id}`: elimina una ruta por UUID. Retorna `200` con `{"msg": "el trayecto fue eliminado"}`.
	- Retorna `404` si no existe.

Todos los cuerpos de error (`400`, `404`, `412`) van bajo la clave `"msg"`, ej. `{"msg": "Las fechas del trayecto no son válidas"}`.

## Pruebas

Ejecutar pruebas unitarias:

```bash
pytest -q
```

Comando usado por CI para cobertura (umbral >= 70%):

```bash
make unittest DIR=routes_app
```

## Autores

- Equipo Cargo tu encargo
- Marcelo César Torres Ortiz (mc.torreso1)
