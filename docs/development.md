---
title: Vista de desarrollo
nav_order: 5
layout: default
---

# Vista de desarrollo

## Estructura del proyecto

Monorepo: un único repositorio con una carpeta independiente por componente, sin acoplamiento de código entre ellas.

```
.
├── .github/workflows/       # Pipelines de evaluación (no modificables, salvo el job por app en ci_evaluador_unit.yml)
├── k8s/                     # Manifiestos de Kubernetes, uno por aplicación
├── docs/                    # Esta documentación técnica (Documentación como Código)
│   └── diagrams/            # Diagramas PlantUML: entities, components, deployment, networks
├── users_app/                # Gestión de usuarios
├── routes_app/               # Gestión de trayectos
├── posts_app/                 # Gestión de publicaciones
├── offers_app/                # Gestión de ofertas
├── config.yaml               # Configuración usada por los pipelines evaluadores
├── makefile                  # Reglas compartidas de lint y pruebas
└── README.md                 # Estructura del repo y despliegue conjunto
```

Cada `<app>/` sigue la misma arquitectura hexagonal:

```
<app>/
├── Dockerfile
├── pyproject.toml            # Dependencias (Poetry)
├── src/
│   ├── config.py              # Configuración por variables de ambiente
│   ├── assembly.py            # Inyección de dependencias
│   ├── errors.py              # Excepciones de dominio
│   ├── domain/
│   │   ├── models/             # Entidades
│   │   ├── ports/               # Interfaces de repositorio
│   │   └── use_cases/           # Un caso de uso por operación de negocio
│   ├── adapters/postgres/      # Implementación real de los puertos (SQLAlchemy)
│   └── entrypoints/api/        # Router y app de FastAPI
└── tests/unit/                # Pruebas de dominio, casos de uso y router
```

## Tabla de tecnologías

| Categoría | Herramienta | Uso |
|---|---|---|
| Lenguaje | Python 3.11 | Todas las aplicaciones |
| Framework web | FastAPI | Exposición de la API REST |
| Gestión de dependencias | Poetry | Instalación y empaquetado por app |
| Pruebas | Pytest + `pytest-cov` | Pruebas unitarias, cobertura mínima 70% |
| Calidad de código | black, isort, ruff, bandit | Formato, orden de imports, lint, seguridad estática |
| Base de datos | PostgreSQL 16 | Una instancia por aplicación, puerto `5432` |
| Acceso a datos | SQLAlchemy (síncrono) + `psycopg2-binary` | Adaptador Postgres de cada app |
| Contenedores | Docker | Build multi-stage por aplicación |
| Orquestación | Kubernetes (Minikube) | Despliegue local, namespace `default` |
| Aislamiento de red | NetworkPolicy | Una política por app, restringe el acceso a su base de datos |
| CI | GitHub Actions | Pruebas unitarias en cada push/PR; evaluadores de k8s y docs manuales |
| Documentación | Markdown + PlantUML + GitHub Pages | Documentación como código |

## Ejecución y desarrollo local

Cada aplicación se ejecuta y prueba de forma independiente:

```bash
poetry --directory=<app> install
poetry --directory=<app> run uvicorn entrypoints.api.main:app --reload --port 9000
```

```bash
make lintcheck DIR=<app>
make unittest DIR=<app>
```

Para el despliegue conjunto de las cuatro aplicaciones sobre Minikube, ver el paso a paso en el [README raíz del repositorio](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/202614-grupo24-proyecto#readme).
