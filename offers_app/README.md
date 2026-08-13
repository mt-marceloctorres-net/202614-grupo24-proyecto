# offers_app

Servicio de gestión de ofertas de "Cargo tu encargo". Una oferta es la propuesta
que hace un usuario para enviar un paquete usando el espacio de equipaje
publicado por otro.

## Estructura

Arquitectura hexagonal. La dependencia siempre apunta hacia adentro: los
adaptadores conocen el dominio, el dominio no conoce a los adaptadores.

```
src/
├── domain/              El negocio, sin saber de HTTP ni de bases de datos
│   ├── models/          Entidades y esquemas de entrada/salida
│   ├── ports/           Interfaces que el dominio necesita (repositorios)
│   └── use_cases/       Un caso de uso por operación del contrato
├── adapters/
│   └── postgres/        Implementación de los puertos contra Postgres
└── entrypoints/
    └── api/             FastAPI: routers y traducción HTTP ↔ dominio
```

## Desarrollo

Desde la **raíz del repositorio**, no desde esta carpeta:

```bash
make lintcheck DIR=offers_app    # black, isort, bandit, ruff
make lintfix   DIR=offers_app    # corrige lo que se pueda automáticamente
make unittest  DIR=offers_app    # pytest con umbral de cobertura del 70%
```

## Correr con Docker

Levanta la app junto con su propia Postgres, desde la **raíz del repositorio**:

```bash
docker compose -f offers_app/docker-compose.yml up --build
```

La documentación interactiva queda en <http://localhost:3000/docs>. Para bajarlo
todo y borrar los datos:

```bash
docker compose -f offers_app/docker-compose.yml down -v
```

Las credenciales de la base se leen de variables de entorno (`DB_HOST`,
`DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`); los valores por defecto de
`src/config.py` solo sirven para correr fuera de contenedor.

`docker-compose.yml` es una comodidad de desarrollo: el evaluador no lo usa,
despliega con los manifiestos de `/k8s` en Minikube.

## Autor

Carlos Alfredo Caicedo Bermúdez — [c.caicedob@uniandes.edu.co](mailto:c.caicedob@uniandes.edu.co)
