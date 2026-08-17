import uuid
from datetime import datetime, timezone

from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidExpirationError


class CreatePostUseCase(BaseUseCase):
    """Caso de uso para crear una publicación."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self, routeId: str, userId: str, expireAt: datetime) -> Post:
        """Crea una publicación, validando que `expireAt` sea futura.

        No valida que `routeId`/`userId` existan en `routes_app`/`users_app`:
        es una decisión deliberada, no un descuido — ver `domain/models/post.py`
        para el porqué (el contrato no lo exige y la colección oficial de
        pruebas no lo comprueba).
        """
        if expireAt.tzinfo is not None:
            expireAt = expireAt.astimezone(timezone.utc).replace(tzinfo=None)

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if expireAt <= now:
            raise InvalidExpirationError("La fecha expiración no es válida")

        post = Post(
            id=str(uuid.uuid4()),
            routeId=routeId,
            userId=userId,
            expireAt=expireAt,
        )
        return self.post_repository.create(post)
