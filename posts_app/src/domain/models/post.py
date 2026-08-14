from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    """Modelo de dominio Publicación.

    `posts_app` no valida que `routeId`/`userId` existan en `routes_app` /
    `users_app` — es una decisión deliberada del equipo (ver AGENTS.md,
    sección "Decisiones contraintuitivas"), no un descuido: un uuid con
    formato válido pero inexistente debe poder crear la publicación.

    No tiene `updatedAt`: a diferencia de Usuario y Trayecto, una
    publicación no se actualiza después de creada.
    """

    id: str | None = None
    routeId: str
    userId: str
    expireAt: datetime
    createdAt: datetime | None = None
