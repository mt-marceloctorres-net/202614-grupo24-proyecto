# Plan de trabajo — Entrega 1

> Nota: este archivo es una guía de trabajo interna del equipo, no es parte de la documentación calificable de `/docs`. No sustituye el enunciado oficial — ante cualquier duda, `docs/first/*` en el repo `documentacion-proyecto-curso` manda.

Fecha límite: **sábado 22 de agosto de 2026, 11:59 pm GMT-5** (release `ProyectoPrimeraEntrega`).

## Agentes disponibles (`.claude/agents/`)

| Agente | Cuándo usarlo |
|---|---|
| `service-scaffolder` | Arrancar la estructura de un microservicio nuevo (hexagonal, como `pets_app`). |
| `api-contract-builder` | Implementar o auditar endpoints contra el contrato oficial de cada API. |
| `k8s-deployer` | Manifiestos de `/k8s`: Deployments, Services, NetworkPolicies, volúmenes. |
| `docs-as-code-writer` | README raíz/por app, `/docs` con las 4 vistas y diagramas PlantUML, `config.yaml`. |
| `test-coverage-guardian` | Pruebas unitarias por app hasta 70% de cobertura + jobs en `ci_evaluador_unit.yml`. |
| `rubric-auditor` | Checklist final antes de crear el release — correrlo siempre antes de entregar. |

## División de trabajo recomendada

El enunciado recomienda una persona por componente (código + BD + contenedor + pipeline + k8s + pruebas + documentación de esa app). Con 4 integrantes:

- Persona 1 → `users_app`
- Persona 2 → `routes_app`
- Persona 3 → `posts_app`
- Persona 4 → `offers_app`

La integración final (manifiestos de `/k8s` conjuntos, README raíz, `config.yaml`, video, release) es trabajo compartido — no de una sola persona.

## Semana 1 — Fundación

- [ ] Confirmar en equipo quién toma cada una de las 4 apps.
- [ ] Leer `docs/first/statement.md`, `restrictions.md` y `technologies.md` completos (todo el equipo, no solo quien entrega).
- [ ] Definir lenguaje/framework (recomendado: Python 3.11 + FastAPI + Poetry, ya hay ejemplo en `pets_app/`). Si se usa otro, validarlo con los tutores por Slack antes de avanzar.
- [ ] `service-scaffolder`: generar la estructura hexagonal de las 4 apps.
- [ ] Actualizar `config.yaml` con nombres de carpeta y autores de cada app (los porcentajes de esfuerzo se declaran al final, no ahora).
- [ ] Cada app corriendo localmente contra su propia Postgres vía Docker/Docker Compose (aún sin Kubernetes).
- [ ] Configurar el tablero Kanban del repositorio y empezar a usarlo — es la fuente de verdad si el equipo no logra acordar el reparto de esfuerzo al final.

## Semana 2 — Contrato de API + pruebas

- [ ] `api-contract-builder`: implementar cada endpoint contra el contrato oficial de su API (`api_users.md`, `api_routes.md`, `api_posts.md`, `api_offers.md`), incluyendo `GET /ping` y `POST /reset` en las 4.
- [ ] `test-coverage-guardian`: pruebas unitarias por app + job en `ci_evaluador_unit.yml` por app, verificar que cada job pasa el 70% de cobertura en el pipeline (no localmente).
- [ ] `k8s-deployer`: primer borrador de los manifiestos en `/k8s` (Deployments + Services de las 4 apps y sus 4 bases de datos).
- [ ] Validar cada API localmente con la colección de Postman de referencia (ver `docs/first/resources.md` del repo de documentación).

## Semana 3 — Integración, redes y documentación

- [ ] `k8s-deployer`: completar NetworkPolicies de aislamiento por base de datos, volúmenes `emptyDir`, y validar todo el despliegue conjunto en Minikube.
- [ ] Correr manualmente el pipeline `Evaluador Implementación Entrega 1` (workflow_dispatch) sobre la rama de trabajo antes de mezclar a `main`.
- [ ] `docs-as-code-writer`: completar README raíz, README por app, y las 4 vistas de `/docs` con sus PlantUML (`components.puml`, `deployment.puml`, `entities.puml`, `networks.puml`). Publicar GitHub Pages del equipo como **privado** y registrar el link en `config.yaml`.
- [ ] Correr manualmente el pipeline `Evaluador Documentación Entrega 1`.
- [ ] `rubric-auditor`: checklist final completo — correrlo con tiempo suficiente para corregir antes del límite, no el mismo día de la entrega.
- [ ] Grabar el video (5–10 min): equipo, arquitectura, demo con Postman de las 4 apps.
- [ ] Definir y declarar el porcentaje de esfuerzo de cada integrante en `config.yaml`.
- [ ] Crear el release `ProyectoPrimeraEntrega` con el video embebido en la descripción, **antes** de la hora límite.

## Recordatorios de restricciones que anulan la entrega

Ver el checklist completo en el agente `rubric-auditor`, pero los más fáciles de olvidar por accidente:

- No tocar `ci_evaluador_entrega1_k8s.yml` ni `ci_evaluador_entrega1_docs.yml`.
- Video embebido en el release, nunca como link externo.
- `config.yaml` completo — sin esto no se puede calificar nada.
- Ninguna app accede a la base de datos de otra directamente.
