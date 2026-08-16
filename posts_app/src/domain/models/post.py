from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    """Modelo de dominio Publicación.

    `posts_app` no valida que `routeId`/`userId` existan en `routes_app` /
    `users_app` — es una decisión deliberada, no un descuido: el contrato
    `api_posts.md` no exige esa validación, y la colección oficial de
    pruebas (`entrega1_posts.json`) tampoco espera un 404 en ese caso. Un
    uuid con formato válido pero inexistente debe poder crear la
    publicación.

    No tiene `updatedAt`: a diferencia de Usuario y Trayecto, una
    publicación no se actualiza después de creada.
    """

    id: str | None = None
    routeId: str
    userId: str
    expireAt: datetime
    createdAt: datetime | None = None
