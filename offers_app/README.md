# Offers App

Microservicio de gestión de ofertas del proyecto **Cargo tu encargo**. Una oferta
es la propuesta que hace un usuario para enviar un paquete aprovechando el
espacio de equipaje que otro publicó. Permite crear ofertas, buscarlas filtrando
por publicación o por dueño, consultarlas y eliminarlas.

Construido en Python 3.11 + FastAPI, con arquitectura hexagonal (dominio /
puertos / adaptadores / entrypoints) y PostgreSQL como base de datos.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Autor](#autor)

## Estructura

La dependencia siempre apunta hacia adentro: los adaptadores conocen el dominio,
el dominio no conoce a los adaptadores. Por eso los casos de uso se pueden probar
con un repositorio en memoria, sin base de datos.

```
offers_app/
├── Dockerfile              # Imagen de la aplicación, expone el puerto 9000
├── docker-compose.yml      # Entorno local: la app y su propia Postgres
├── pyproject.toml          # Dependencias (Poetry)
├── src/
│   ├── config.py           # Configuración por variables de ambiente
│   ├── assembly.py         # Único punto donde se elige el adaptador concreto
│   ├── errors.py           # Excepciones de dominio
│   ├── domain/
│   │   ├── models/         # Entidad Oferta y modelos de entrada/salida
│   │   ├── ports/          # Interfaz OfferRepositoryPort
│   │   └── use_cases/      # Un caso de uso por operación del contrato
│   ├── adapters/
│   │   └── postgres/       # Implementación del puerto con SQLAlchemy
│   └── entrypoints/
│       └── api/            # Routers de FastAPI y traducción HTTP ↔ dominio
└── tests/
    └── unit/               # Dominio, casos de uso, adaptador y router
```

## Ejecución

### Local, con Poetry

```bash
poetry install
PYTHONPATH=$(pwd)/src poetry run uvicorn entrypoints.api.main:app --host 0.0.0.0 --port 9000
```

El API queda en `http://localhost:9000` y la documentación interactiva en
`http://localhost:9000/docs`. Necesita una Postgres accesible: las tablas se
crean solas al arrancar, pero si la base no responde el proceso falla de
inmediato en vez de aceptar peticiones que se caerían una por una.

### Variables de ambiente

| Variable | Default | Descripción |
|---|---|---|
| `APP_NAME` | `Offers app` | Nombre de la aplicación |
| `LOG_LEVEL` | `DEBUG` | Nivel de logging |
| `DB_HOST` | `localhost` | Host de Postgres |
| `DB_PORT` | `5432` | Puerto de Postgres |
| `DB_NAME` | `offers_db` | Nombre de la base de datos |
| `DB_USER` | `postgres` | Usuario de la base de datos |
| `DB_PASSWORD` | `postgres` | Contraseña de la base de datos |

Los valores por defecto sirven para correr fuera de contenedor. En Kubernetes
cada uno llega por variable de ambiente, y `DB_HOST` apunta al nombre del
Service de la base de datos.

### Con Docker Compose

Levanta la aplicación junto con su propia Postgres. Desde la raíz del
repositorio:

```bash
docker compose -f offers_app/docker-compose.yml up -d --build
docker compose -f offers_app/docker-compose.yml logs -f offers-app
docker compose -f offers_app/docker-compose.yml down -v
```

Es una comodidad de desarrollo, no la forma en que se despliega el proyecto.

### Con Docker

```bash
docker build --rm --platform linux/amd64 -t offers_app:v1.0.0 -f Dockerfile --label version=v1.0.0 .
docker run --platform linux/amd64 -p 9000:9000 \
  -e DB_HOST=<host> -e DB_PORT=5432 -e DB_NAME=offers_db -e DB_USER=postgres -e DB_PASSWORD=postgres \
  offers_app:v1.0.0
```

### En Kubernetes (Minikube)

```bash
minikube image load offers_app:v1.0.0
kubectl apply -f ../k8s/offers_app.yaml
```

Despliega `offers-app` y `offers-db` con aislamiento de red: solo `offers-app`
puede conectarse a `offers-db`, por el puerto 5432. El API queda expuesto en el
NodePort `30003`.

## Uso

API REST bajo el prefijo `/offers`, contra el contrato oficial del curso
(`api_offers.md`):

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/offers` | Crea una oferta |
| GET | `/offers?post={postId}&owner={userId}` | Lista ofertas; ambos filtros son opcionales y se combinan |
| GET | `/offers/{id}` | Consulta una oferta |
| DELETE | `/offers/{id}` | Elimina una oferta |
| GET | `/offers/count` | Cuenta las ofertas almacenadas |
| GET | `/offers/ping` | Verifica que el servicio esté arriba |
| POST | `/offers/reset` | Elimina todas las ofertas |

### Cómo se reparten los errores

El servicio distingue dos clases de problema, tal como pide el contrato:

- **400** cuando el cuerpo tiene un problema de **forma**: falta un campo, llega
  con otro tipo, o `postId` y `userId` no tienen formato uuid.
- **412** cuando un campo tiene la forma correcta pero un **valor** inaceptable:
  un tamaño que no es `LARGE`, `MEDIUM` ni `SMALL`, una oferta negativa, o una
  descripción de más de 140 caracteres.
- **404** cuando el identificador es un uuid válido pero no existe esa oferta.
  No confundir con el 400, que es para un identificador mal formado.

Una búsqueda sin resultados responde **200** con una lista vacía: no encontrar
nada es una búsqueda exitosa, no un error.

### Ejemplo

```bash
curl -X POST http://localhost:9000/offers \
  -H "Content-Type: application/json" \
  -d '{
    "postId": "11111111-1111-1111-1111-111111111111",
    "userId": "22222222-2222-2222-2222-222222222222",
    "description": "Caja de libros",
    "size": "MEDIUM",
    "fragile": false,
    "offer": 25.5
  }'
```

Responde `201` con los tres campos del contrato:

```json
{
  "id": "e25ce16f-79ee-4c47-b23f-808c7aa9068a",
  "userId": "22222222-2222-2222-2222-222222222222",
  "createdAt": "2026-08-13T23:16:55.250910"
}
```

Las fechas se guardan y se devuelven en UTC.

Para probar el API completo, importa en Postman la colección oficial
`entrega1_offers.json` y apunta `OFFERS_PATH` a tu instancia.

## Pruebas

Desde la **raíz del repositorio**:

```bash
make lintcheck DIR=offers_app    # black, isort, bandit, ruff
make lintfix   DIR=offers_app    # corrige lo que se pueda automáticamente
make unittest  DIR=offers_app    # pytest con umbral de cobertura del 70%
```

75 pruebas unitarias, cobertura **95.41%**. Cubren las cuatro capas por
separado: las reglas de negocio del dominio, cada caso de uso contra un
repositorio en memoria, el adaptador contra SQLite en memoria —SQL real, sin
simulaciones— y los siete endpoints con `TestClient`, que pasan por la
serialización real de FastAPI.

Se ejecutan en el pipeline `ci_evaluador_unit.yml`, job `offers_app`, en cada
push y cada pull request hacia `main`.

## Autor

Carlos Alfredo Caicedo Bermúdez — [c.caicedob@uniandes.edu.co](mailto:c.caicedob@uniandes.edu.co)
