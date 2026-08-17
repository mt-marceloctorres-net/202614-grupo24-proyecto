from typing import Optional

from adapters.postgres.models import PostModel, utcnow
from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort


def _model_to_entity(model: PostModel) -> Post:
    return Post(
        id=model.id,
        routeId=model.routeId,
        userId=model.userId,
        expireAt=model.expireAt,
        createdAt=model.createdAt,
    )


class PostgresPostRepositoryAdapter(PostRepositoryPort):
    """Implementación del repositorio de publicaciones sobre Postgres."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create(self, post: Post) -> Post:
        """Crea una nueva publicación."""
        with self.session_factory() as session:
            model = PostModel(
                id=post.id,
                routeId=post.routeId,
                userId=post.userId,
                expireAt=post.expireAt,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return _model_to_entity(model)

    def get_by_id(self, post_id: str) -> Optional[Post]:
        """Obtiene una publicación por su id."""
        with self.session_factory() as session:
            model = session.get(PostModel, post_id)
            return _model_to_entity(model) if model else None

    def list(
        self,
        expire: Optional[bool] = None,
        route_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> list[Post]:
        """Lista publicaciones, filtrando (AND) por expiración/trayecto/dueño."""
        with self.session_factory() as session:
            query = session.query(PostModel)
            if route_id is not None:
                query = query.filter(PostModel.routeId == route_id)
            if owner_id is not None:
                query = query.filter(PostModel.userId == owner_id)
            if expire is not None:
                now = utcnow()
                if expire:
                    query = query.filter(PostModel.expireAt <= now)
                else:
                    query = query.filter(PostModel.expireAt > now)
            return [_model_to_entity(model) for model in query.all()]

    def delete(self, post_id: str) -> bool:
        """Elimina una publicación por id. Retorna False si no existía."""
        with self.session_factory() as session:
            model = session.get(PostModel, post_id)
            if not model:
                return False
            session.delete(model)
            session.commit()
            return True

    def count(self) -> int:
        """Cuenta cuántas publicaciones hay almacenadas."""
        with self.session_factory() as session:
            return session.query(PostModel).count()

    def delete_all(self) -> None:
        """Elimina todas las publicaciones."""
        with self.session_factory() as session:
            session.query(PostModel).delete()
            session.commit()
