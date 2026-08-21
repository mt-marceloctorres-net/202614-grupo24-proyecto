---
title: Home
layout: home
nav_order: 1
permalink: /
---

# Cargo tu encargo

Cargo tu encargo conecta a personas que necesitan enviar un paquete con viajeros que ya tienen planeado un trayecto y les sobra espacio de equipaje. Un usuario publica una oferta de envío sobre un trayecto existente, y otro usuario con espacio disponible responde con una oferta de transporte.

Este proyecto implementa el sistema en cuatro aplicaciones independientes (usuarios, trayectos, publicaciones y ofertas), cada una dueña de su propia base de datos, desplegadas como contenedores independientes sobre Kubernetes.

## Equipo

**Grupo**: Cargo tu encargo
**Líder**: Omar Fernando Muñoz (`of.munoz`)

| Integrante | Usuario Uniandes | Aplicación a cargo |
|---|---|---|
| Carlos Alfredo Caicedo Bermudez | `c.caicedob` | `offers_app`: gestión de ofertas |
| Omar Fernando Muñoz | `of.munoz` | `users_app`: gestión de usuarios |
| Marco Tulio Torres Meneses | `mar-torr` | `posts_app`: gestión de publicaciones |
| Marcelo Cesar Torres Ortiz | `mc.torreso1` | `routes_app`: gestión de trayectos |

### Carlos Alfredo Caicedo Bermudez

- **GitHub**: [@CaicedoBz](https://github.com/CaicedoBz)
- **Correo Uniandes**: `c.caicedob@uniandes.edu.co`
- **Rol actual**: _[Carlos completa esto]_
- **Intereses en ingeniería de software**: _[Carlos completa esto]_

### Omar Fernando Muñoz

- **GitHub**: [@ofmunozm](https://github.com/ofmunozm)
- **Correo Uniandes**: `of.munoz@uniandes.edu.co`
- **Rol actual**: Product Manager en Mareigua, en el sector fintech. Coordino el desarrollo de productos digitales relacionados con procesamiento de datos y modelos predictivos, para los mercados colombiano y mexicano. Profesional en Finanzas de la Universidad Externado de Colombia y estudiante de la Maestría en Ingeniería de Software.
- **Intereses en ingeniería de software**: Computación en la nube, datos e inteligencia artificial. Experiencia en el desarrollo de productos para la recolección y limpieza de datos y la generación de scores crediticios, donde la calidad del dato y la trazabilidad del modelo son determinantes. Interés particular en comprender y aplicar arquitecturas nativas en la nube para llevar ese tipo de productos a escala.

### Marco Tulio Torres Meneses

- **GitHub**: [@mttm-maia](https://github.com/mttm-maia)
- **Correo Uniandes**: `mar-torr@uniandes.edu.co`
- **Rol actual**: Ingeniero Eléctrico y Electrónico de la Universidad de los Andes, Especialista en Sistemas de Transmisión y Distribución de Energía Eléctrica y estudiante de la Maestría en Inteligencia Artificial de la Universidad de los Andes. Ingeniero de Diseño, a nivel de Especialista Electromecánico, en el mercado de Potencia y Energía de WSP Perú, con participación en proyectos de diseño, ingeniería y supervisión de obra de líneas de transmisión en la región (Perú, Colombia y Chile).
- **Intereses en ingeniería de software**: Inteligencia artificial aplicada a la ingeniería y despliegue de aplicaciones en la nube. Interés en adquirir las habilidades necesarias para impulsar el desarrollo de aplicaciones basadas en herramientas de inteligencia artificial que resuelvan problemas de diversos tipos y contextos, tanto a nivel general como en los servicios de ingeniería de la empresa en la que trabajo. Específicamente, interés en implementar el despliegue de este tipo de aplicaciones en la nube, para facilitar su uso sin limitaciones de ubicación, espacio o tiempo, de manera segura y confiable.

### Marcelo Cesar Torres Ortiz

- **GitHub**: [@mc-torreso1-uniandes-edu-co](https://github.com/mc-torreso1-uniandes-edu-co)
- **Correo Uniandes**: `mc.torreso1@uniandes.edu.co`
- **Rol actual**: Ingeniero Civil de la Universidad Católica de Colombia, Especialista en Sistemas de Información Geográfica de la Universidad Antonio Nariño, Estudiante de la Maestría en Inteligencia Artificial de la Universidad de los Andes, con experiencia en desarrollo de software y análisis de datos. Arquitecto de Soluciones Geográficas en el área de Servicios Profesionales de Esri Colombia, Ecuador y Panamá, distribuidor exclusivo del software ArcGIS para los tres países. Participación en proyectos de desarrollo de software y análisis de datos para clientes del sector público y privado, incluyendo entidades gubernamentales, empresas de telecomunicaciones y organizaciones sin ánimo de lucro. 
- **Intereses en ingeniería de software**: Experiencia que incluye el diseño e implementación de soluciones geoespaciales, análisis de datos geográficos y desarrollo de aplicaciones web, móviles y de escritorio. Participación en proyectos de investigación relacionados con la inteligencia artificial y el aprendizaje automático aplicados a problemas geoespaciales. Apasionado por la tecnología y su aplicación para resolver problemas del mundo real, y comprometido con el aprendizaje continuo y la mejora constante en la carrera profesional. Especificamente, interés en el desarrollo de aplicaciones nativas en la nube para brindar asesoría a los clientes en la implementación de soluciones geoespaciales y análisis de datos geográficos en la nube.

### Reglas de equipo

1. **Protección de la rama `main` y trabajo mediante ramas.** La rama `main` contendrá únicamente versiones estables e integradas del proyecto. Ningún integrante realizará cambios directamente sobre ella. Cada tarea deberá desarrollarse en una rama independiente creada desde `main`, utilizando una convención como `feature/<id>-descripcion`, `fix/<id>-descripcion` o `docs/<id>-descripcion`. Antes de solicitar integración, la rama deberá actualizarse con los cambios recientes de `main` y los conflictos deberán resolverse en la propia rama de trabajo.
2. **Toda actividad debe estar asociada al tablero Kanban.** Ningún desarrollo deberá comenzar sin que exista previamente una tarea registrada en el Kanban y con un responsable asignado. La tarjeta deberá permitir identificar la rama y el Pull Request relacionados. Como mínimo se manejarán los estados `Todo`, `In progress`, `Under Review` y `Done`, manteniendo siempre el tablero sincronizado con el estado real del trabajo.
3. **Commits pequeños, coherentes y descriptivos.** Cada commit deberá representar un cambio funcional o técnico específico, evitando mezclar modificaciones no relacionadas. Los mensajes deberán describir claramente la intención del cambio, utilizando convenciones como `feat:`, `fix:`, `test:`, `docs:` o `refactor:`. Se deberá evitar acumular grandes cantidades de cambios en un único commit.
4. **Pull Request obligatorio para integrar cambios.** Todo cambio destinado a `main` deberá incorporarse mediante un Pull Request. Cada Pull Request deberá estar asociado preferiblemente con una sola tarea o con un conjunto pequeño de tareas estrechamente relacionadas, e incluir como mínimo la descripción de los cambios, la referencia a la tarea del Kanban, las pruebas realizadas y cualquier consideración relevante para su revisión.
5. **Revisión y aprobación por otro integrante del equipo.** El autor de un Pull Request no deberá ser su único revisor. Al menos otro integrante del equipo deberá validar el código antes de integrarlo, verificando funcionamiento, calidad, cumplimiento de los contratos de las APIs, consistencia con la arquitectura definida y ausencia de modificaciones no autorizadas sobre los archivos suministrados por el curso.
6. **Validaciones obligatorias y protección de los artefactos base.** No se deberá realizar el merge de un Pull Request mientras existan pruebas unitarias, linters o pipelines fallidos. Cada aplicación deberá mantener la cobertura mínima exigida por el proyecto. Los archivos base suministrados por el curso deberán conservarse según sus restricciones: los workflows que no admitan modificación permanecerán intactos, las reglas existentes del `makefile` no serán alteradas y, en los archivos donde se permita extensión, solamente se adicionará el contenido necesario.
7. **Cierre de tareas y responsabilidad posterior al merge.** Una tarea únicamente podrá marcarse como `Done` después de que el Pull Request correspondiente haya sido integrado en `main` y las validaciones hayan terminado correctamente. El responsable de la tarea deberá verificar que el cambio integrado funcione adecuadamente. Si posteriormente se detecta un defecto, deberá registrarse una nueva tarea en el Kanban y realizarse la corrección mediante una nueva rama y un nuevo Pull Request, evitando correcciones directas sobre `main`.
8. **Propiedad por aplicación.** Cada aplicación es responsabilidad de su autor declarado en `config.yaml`; cambios sobre una aplicación que no es la propia se coordinan primero con su dueño.

{: .alert }
Cualquier cambio que no cumpla con estas reglas será considerado una violación de las normas de trabajo del equipo y podrá ser revertido. Sin embargo, antes de ejecutar la reversión se discutirá con los miembros del equipo, y se aprobará mediante consenso o votación. Se espera que todos los miembros del equipo cumplan con estas reglas para garantizar la calidad y el éxito del proyecto.

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
