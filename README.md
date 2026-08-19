# Cargo tu encargo

Sistema para conectar personas que necesitan enviar un paquete con viajeros que ya tienen un trayecto planeado y les sobra espacio de equipaje. Cuatro aplicaciones independientes (usuarios, trayectos, publicaciones, ofertas), cada una dueña de su propia base de datos, desplegadas como contenedores sobre Kubernetes.

## Tabla de contenido

- [Cargo tu encargo](#cargo-tu-encargo)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Archivo de configuración](#archivo-de-configuración)
  - [Estructura de cada aplicación](#estructura-de-cada-aplicación)
  - [Despliegue conjunto en Minikube](#despliegue-conjunto-en-minikube)
  - [Pruebas](#pruebas)
  - [Documentación técnica](#documentación-técnica)
  - [Decisión de tecnologías](#decisión-de-tecnologías)

## Estructura del Proyecto

```
.
├── .github/workflows/       # Pipelines del repositorio
├── k8s/                     # Manifiestos de Kubernetes, uno por aplicación
├── docs/                    # Documentación técnica (Documentación como Código)
│   └── diagrams/            # Diagramas PlantUML: entities, components, deployment, networks
├── users_app/                # Gestión de usuarios
├── routes_app/                # Gestión de trayectos
├── posts_app/                  # Gestión de publicaciones
├── offers_app/                  # Gestión de ofertas
├── pets_app/                     # Ejemplo del curso (Python/Poetry/FastAPI/Pytest), no se despliega
├── .vale.ini                 # Configuración para Vale. NO MODIFICAR
├── config.yaml               # Configuración del repositorio. El archivo más importante
├── makefile                  # Scripts para evaluación. NO MODIFICAR las reglas actuales
└── README.md                 # Este archivo
```

1. **`.github/workflows`**: los archivos en esta carpeta no se pueden modificar a excepción de `ci_evaluador_unit.yml`, usado para agregar un job por cada aplicación.
   * `ci_evaluador_entrega1_k8s.yml` verifica la configuración de k8s y ejecuta pruebas sobre cada aplicación. Su modificación anula la entrega.
   * `ci_evaluador_entrega1_docs.yml` verifica que los diagramas de la documentación contengan los componentes esperados y hace revisión gramatical del markdown. Su modificación anula la entrega.
   * `ci_evaluador_unit.yml` ejecuta las pruebas unitarias, con un job por aplicación.
2. **`k8s/`**: un archivo de manifiestos por aplicación (`users_app.yaml`, `routes_app.yaml`, `posts_app.yaml`, `offers_app.yaml`), cada uno con su Deployment + Service de app, Deployment + Service de base de datos, y su `NetworkPolicy`.
3. **`docs/`**: documentación técnica. `docs/README.md` es la portada publicada en GitHub Pages; `docs/diagrams/` contiene los `.puml` de las 4 vistas.
4. **`<aplicación>_app/`**: una carpeta por aplicación, todas construidas en Python 3.11 + FastAPI con arquitectura hexagonal — ver más abajo.
5. **`makefile`**: usado por los pipelines evaluadores. No se modifican las reglas existentes, sí se pueden agregar nuevas.

## Archivo de configuración

El archivo `config.yaml` es el archivo más importante en el repositorio. Contiene la configuración que usan los pipelines para evaluar la entrega y define la calificación de cada miembro del equipo. Si no está correctamente configurado, la entrega no puede ser calificada y la nota será de cero.

## Estructura de cada aplicación

Cada aplicación sigue las mismas reglas:

1. Carpeta independiente, construida en el lenguaje de preferencia del equipo. `pets_app/` es el ejemplo del curso en `Python`, `Poetry`, `FastAPI` y `Pytest` — no se despliega, es solo referencia de estructura.
2. `Dockerfile` en la raíz de la carpeta de la aplicación (no en otra ubicación).
3. El nombre de la carpeta, el nombre de la imagen y su tag están registrados en `config.yaml`, y deben coincidir con lo usado en el manifiesto de `k8s/`.

Las 4 aplicaciones del equipo (`users_app`, `routes_app`, `posts_app`, `offers_app`) siguen arquitectura hexagonal (dominio / puertos / adaptadores / entrypoints) — ver la vista de desarrollo en la [documentación técnica](https://refactored-dollop-qwj93z8.pages.github.io/) para el detalle de la estructura interna y la tabla de tecnologías.

## Despliegue conjunto en Minikube

Requiere Docker, Minikube y `kubectl`. Todas las apps exponen su API en el puerto `9000` dentro del contenedor y su base de datos Postgres en `5432`.

1. **Construir las 4 imágenes** (nombres y tags según `config.yaml`, todas `v1.0.0`):

   ```bash
   docker build -t users_app:v1.0.0 ./users_app
   docker build -t routes_app:v1.0.0 ./routes_app
   docker build -t posts_app:v1.0.0 ./posts_app
   docker build -t offers_app:v1.0.0 ./offers_app
   ```

2. **Cargar las imágenes en Minikube** (no necesitan un registry):

   ```bash
   minikube image load users_app:v1.0.0
   minikube image load routes_app:v1.0.0
   minikube image load posts_app:v1.0.0
   minikube image load offers_app:v1.0.0
   ```

3. **Aplicar los manifiestos** — cada uno crea su Deployment + Service de app, Deployment + Service de base de datos (Postgres, puerto `5432`), y su `NetworkPolicy` de aislamiento, todo en el namespace `default`:

   ```bash
   kubectl apply -f k8s/users_app.yaml
   kubectl apply -f k8s/routes_app.yaml
   kubectl apply -f k8s/posts_app.yaml
   kubectl apply -f k8s/offers_app.yaml
   ```

4. **Verificar que las 8 cargas (4 apps + 4 bases de datos) están sanas**:

   ```bash
   kubectl get pods,svc,networkpolicy -n default
   ```

5. **Acceder a cada API** desde fuera del clúster, por el `Service` `NodePort` de cada app. Los cuatro siguen el modelo de red oficial del curso (`docs/images/network.png`), reflejado en `docs/diagrams/networks.puml`: `users=30000`, `posts=30001`, `routes=30002`, `offers=30003`, todos con `port: 80` en el Service y `targetPort: 9000` en el contenedor.

   ```bash
   curl http://$(minikube ip):30000/users/ping    # users_app
   curl http://$(minikube ip):30001/posts/ping    # posts_app
   curl http://$(minikube ip):30002/routes/ping   # routes_app
   curl http://$(minikube ip):30003/offers/ping   # offers_app
   ```

   En macOS con el driver de Docker la IP del nodo no es alcanzable directamente; en ese caso use `minikube service <app>-app-service --url` o `kubectl port-forward svc/<app>-app-service 9000:80`.

   Para probar el API completo de cada aplicación, importe en Postman la colección oficial correspondiente (`entrega1_users.json`, `entrega1_routes.json`, `entrega1_posts.json`, `entrega1_offers.json`) y apunte la variable de entorno al puerto expuesto.

6. **Limpiar** (opcional):

   ```bash
   kubectl delete -f k8s/users_app.yaml -f k8s/routes_app.yaml -f k8s/posts_app.yaml -f k8s/offers_app.yaml
   ```

## Pruebas

Cada aplicación se prueba de forma independiente, sin necesitar Postgres real (usan un repositorio en memoria para las pruebas unitarias):

```bash
make lintcheck DIR=<app>   # black, isort, ruff, bandit
make unittest DIR=<app>    # pytest + cobertura, mínimo 70%
```

Donde `<app>` es `users_app`, `routes_app`, `posts_app` u `offers_app`. Estas mismas reglas corren automáticamente en `ci_evaluador_unit.yml` en cada push/PR a `main`.

## Documentación técnica

Las 4 vistas de arquitectura (información, funcional, despliegue, desarrollo), con sus diagramas PlantUML, están publicadas en GitHub Pages:

**https://refactored-dollop-qwj93z8.pages.github.io/**

(sitio privado — visible solo para quien tenga acceso al repositorio).

## Decisión de tecnologías

El equipo (Cargo tu encargo) construyó las 4 aplicaciones (`users_app`, `routes_app`, `posts_app`, `offers_app`) con:

- **Lenguaje/framework**: Python 3.11 + FastAPI
- **Gestión de dependencias**: Poetry
- **Pruebas**: Pytest
- **Base de datos**: PostgreSQL, una por aplicación
- **Acceso a datos**: SQLAlchemy (síncrono) + `psycopg2-binary` como driver, en el adaptador Postgres de cada app
- **Arquitectura**: hexagonal (dominio / puertos / adaptadores / entrypoints), siguiendo el patrón de `pets_app/` pero con adaptador Postgres en vez de memoria

> Ver `users_app/` como ejemplo concreto de este patrón — es la referencia de estructura para `routes_app`, `posts_app` y `offers_app`.
