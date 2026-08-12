# Users App

Microservicio de gestión de usuarios del proyecto **Cargo tu encargo**. Permite crear usuarios, autenticarlos por token, consultar su información y administrar su ciclo de vida. Construido en Python 3.11 + FastAPI, con arquitectura hexagonal (dominio / puertos / adaptadores / entrypoints) y PostgreSQL como base de datos, siguiendo el patrón de `pets_app/` del repositorio base.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Autor](#autor)

## Estructura

```
users_app/
├── Dockerfile              # Build multi-stage, rootless
├── pyproject.toml          # Dependencias (Poetry)
├── src/
│   ├── config.py           # Configuración por variables de ambiente
│   ├── assembly.py         # Inyección de dependencias (wiring de casos de uso)
│   ├── errors.py           # Excepciones de dominio
│   ├── security.py         # Cifrado de contraseñas (PBKDF2 + salt)
│   ├── domain/
│   │   ├── models/         # Entidad Usuario (Pydantic)
│   │   ├── ports/          # Interfaz UserRepositoryPort
│   │   └── use_cases/      # Un caso de uso por operación
│   ├── adapters/
│   │   └── postgres/       # Implementación real del puerto (SQLAlchemy)
│   └── entrypoints/
│       └── api/            # Routers de FastAPI
└── tests/
    └── unit/                # Pruebas de dominio, casos de uso y router
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
| `APP_NAME` | `Users app` | Nombre de la aplicación |
| `LOG_LEVEL` | `DEBUG` | Nivel de logging |
| `DB_HOST` | `localhost` | Host de Postgres |
| `DB_PORT` | `5432` | Puerto de Postgres |
| `DB_NAME` | `users_db` | Nombre de la base de datos |
| `DB_USER` | `postgres` | Usuario de la base de datos |
| `DB_PASSWORD` | `postgres` | Contraseña de la base de datos |
| `TOKEN_EXPIRATION_MINUTES` | `60` | Minutos de vigencia del token de sesión |

### Con Docker

```bash
docker build --rm --platform linux/amd64 -t users_app:v1.0.0 -f Dockerfile --target runner --label version=v1.0.0 .
docker run --platform linux/amd64 -p 9000:9000 \
  -e DB_HOST=<host> -e DB_PORT=5432 -e DB_NAME=users_db -e DB_USER=postgres -e DB_PASSWORD=postgres \
  users_app:v1.0.0
```

### En Kubernetes (Minikube)

```bash
minikube image load users_app:v1.0.0
kubectl apply -f ../k8s/users_app.yaml
```

Despliega `users-app` + `users-db` con aislamiento de red (solo `users-app` puede conectarse a `users-db`).

## Uso

API REST bajo el prefijo `/users`, contra el contrato oficial (`api_users.md` del curso):

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/users` | Crea un usuario |
| PATCH | `/users/{id}` | Actualiza datos públicos de un usuario |
| POST | `/users/auth` | Genera un token de sesión |
| GET | `/users/me` | Consulta el usuario dueño del token (header `Authorization: Bearer <token>`) |
| GET | `/users/count` | Cuenta los usuarios almacenados |
| GET | `/users/ping` | Healthcheck |
| POST | `/users/reset` | Elimina todos los usuarios |

La contraseña se guarda cifrada (PBKDF2-SHA256 con salt aleatorio, nunca en texto plano) y el token de sesión es una cadena aleatoria (`uuid4`), no JWT.

Para probar el API completo, importa en Postman la colección oficial `entrega1_users.json` y apunta `USERS_PATH` a tu instancia.

## Pruebas

```bash
poetry install
poetry run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing
```

35 pruebas unitarias (modelo de dominio, 6 casos de uso, y router con dependencias falsas — sin necesitar Postgres real), cobertura actual **82.77%**. Se ejecutan automáticamente en el pipeline `ci_evaluador_unit.yml` (job `users_app`) en cada push/PR a `main`.

## Autor

Omar Fernando Muñoz — [of.munoz@uniandes.edu.co](mailto:of.munoz@uniandes.edu.co)
