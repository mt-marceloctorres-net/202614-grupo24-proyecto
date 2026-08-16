---
title: Home
layout: home
nav_order: 1
---

# Cargo tu encargo

Cargo tu encargo conecta a personas que necesitan enviar un paquete con viajeros que ya tienen planeado un trayecto y les sobra espacio de equipaje. Un usuario publica una oferta de envío sobre un trayecto existente, y otro usuario con espacio disponible responde con una oferta de transporte.

Este proyecto implementa el sistema en cuatro aplicaciones independientes — usuarios, trayectos, publicaciones y ofertas — cada una dueña de su propia base de datos, desplegadas como contenedores independientes sobre Kubernetes.

## Equipo

| Integrante | Usuario Uniandes | Aplicación a cargo |
|---|---|---|
| Carlos Alfredo Caicedo Bermudez | `c.caicedob` | `offers_app` — gestión de ofertas |
| Omar Fernando Muñoz | `of.munoz` | `users_app` — gestión de usuarios |
| Marco Tulio Torres Meneses | `mar-torr` | `posts_app` — gestión de publicaciones |
| Marcelo Cesar Torres Ortiz | `mc.torreso1` | `routes_app` — gestión de trayectos |

## Tecnologías

- **Lenguaje / framework**: Python 3.11 + FastAPI
- **Gestión de dependencias**: Poetry
- **Pruebas**: Pytest, con cobertura medida por `pytest-cov` (mínimo 70% por aplicación)
- **Base de datos**: PostgreSQL, una instancia independiente por aplicación
- **Acceso a datos**: SQLAlchemy (síncrono) + `psycopg2-binary` como driver
- **Arquitectura**: hexagonal (dominio / puertos / adaptadores / entrypoints) en las cuatro aplicaciones
- **Contenedores y despliegue**: Docker, orquestado con Kubernetes sobre Minikube
- **Documentación**: Documentación como código, escrita en Markdown y publicada con GitHub Pages; diagramas en PlantUML

Consulte el [README raíz del repositorio](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/202614-grupo24-proyecto#readme) para el paso a paso de ejecución y despliegue conjunto, y el `README.md` de cada aplicación para su detalle individual.

## Vistas de arquitectura

| Vista | Contenido |
|---|---|
| [Vista de información](./information.md) | Entidades del sistema y sus atributos |
| [Vista funcional](./functional.md) | Componentes del sistema y sus relaciones |
| [Vista de despliegue](./deployment.md) | Despliegue en Kubernetes y políticas de red |
| [Vista de desarrollo](./development.md) | Estructura de carpetas y tabla de tecnologías |
