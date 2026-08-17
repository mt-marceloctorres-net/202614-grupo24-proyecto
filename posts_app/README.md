# Posts App

Microservicio de gestión de publicaciones del proyecto **Cargo tu encargo**. Permite crear publicaciones de un usuario sobre un trayecto, consultarlas, filtrarlas y eliminarlas. Construido en Python 3.11 + FastAPI, con arquitectura hexagonal (dominio / puertos / adaptadores / entrypoints) y PostgreSQL como base de datos, siguiendo el patrón de `users_app/`.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Autor](#autor)

## Estructura

```
posts_app/
├── Dockerfile              # Build multi-stage, rootless
├── pyproject.toml          # Dependencias (Poetry)
├── src/
│   ├── config.py           # Configuración por variables de ambiente (pydantic-settings)
│   ├── assembly.py         # Inyección de dependencias (wiring de casos de uso)
│   ├── errors.py           # Excepciones de dominio
│   ├── domain/
│   │   ├── models/         # Entidad Publicación (Pydantic)
│   │   ├── ports/          # Interfaz PostRepositoryPort
│   │   └── use_cases/      # Un caso de uso por operación
│   ├── adapters/
│   │   └── postgres/       # Implementación real del puerto (SQLAlchemy)
│   └── entrypoints/
│       └── api/            # Router de FastAPI
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

### En Kubernetes (Minikube)

```bash
minikube image load posts_app:v1.0.0
kubectl apply -f ../k8s/posts_app.yaml
```

Despliega `posts-app` (Service `posts-app-service`) + `posts-db` (Service `posts-db-service`), con aislamiento de red mediante la `NetworkPolicy` `posts-network`: solo `posts-app` puede conectarse a `posts-db`.

El aislamiento se probó manualmente en un clúster real de Minikube con CNI Calico (`minikube start --cni=calico`) y quedó confirmado: pods `1/1 Running` y la política bloqueando el tráfico no autorizado. Sin un CNI que soporte `NetworkPolicy` (el driver por defecto de Minikube no lo soporta), estas políticas se aceptan pero no se aplican — vale la pena tenerlo presente antes de repetir la validación.

## Uso

API REST bajo el prefijo `/posts`, contra el contrato oficial (`api_posts.md` del curso):

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/posts` | Crea una publicación |
| GET | `/posts` | Ve y filtra publicaciones (`expire`, `route`, `owner`, todos opcionales) |
| GET | `/posts/{id}` | Consulta una publicación |
| DELETE | `/posts/{id}` | Elimina una publicación |
| GET | `/posts/count` | Cuenta las publicaciones almacenadas |
| GET | `/posts/ping` | Healthcheck |
| POST | `/posts/reset` | Elimina todas las publicaciones |

`posts_app` no valida que `routeId`/`userId` existan en `routes_app`/`users_app`: es una decisión deliberada, no una omisión — el contrato `api_posts.md` no la exige y la colección oficial de pruebas (`entrega1_posts.json`) tampoco la comprueba. Sí se valida que ambos tengan **formato** uuid (400 si no), aunque no se compruebe que existan. La creación de una publicación devuelve `412` con el cuerpo `{"msg": "La fecha expiración no es válida"}` si `expireAt` no es una fecha futura.

Para probar el API completo, importa en Postman la colección oficial `entrega1_posts.json` y apunta la variable de entorno correspondiente a tu instancia.

## Pruebas

```bash
poetry install
poetry run pytest --cov=src -v -s --cov-report term-missing
```

39 pruebas unitarias (modelo de dominio, configuración, 6 casos de uso con un repositorio falso en memoria, y router con `TestClient` y `dependency_overrides` — sin necesitar Postgres real), cobertura actual **76.71%**. Se ejecutan automáticamente en el pipeline `ci_evaluador_unit.yml` (job `posts_app`) en cada push/PR a `main`.

## Autor

Marco Torres — [mar-torr@uniandes.edu.co](mailto:mar-torr@uniandes.edu.co)
