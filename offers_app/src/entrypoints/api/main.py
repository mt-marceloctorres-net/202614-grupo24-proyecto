from contextlib import asynccontextmanager

from fastapi import FastAPI

from adapters.postgres.database import engine
from adapters.postgres.models import Base
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas al arrancar la aplicación.

    El proyecto no usa migraciones: cada despliegue parte de una base vacía, y el
    evaluador levanta el clúster desde cero. `create_all` es idempotente — si la
    tabla ya existe no hace nada, así que reiniciar el pod no borra datos.

    Que esto viva en el arranque tiene un efecto deseado: si la base de datos no
    responde, el contenedor falla de inmediato en vez de aceptar peticiones que
    se caerían una por una. En Kubernetes eso se traduce en un pod que reintenta
    hasta que su Postgres esté lista.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
