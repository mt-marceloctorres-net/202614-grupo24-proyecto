import uuid
from typing import Optional

from adapters.postgres.models import OfferModel, utcnow
from domain.models.offer import Offer, PackageSize
from domain.ports.offer_repository_port import OfferRepositoryPort


class PostgresOfferRepositoryAdapter(OfferRepositoryPort):
    """Implementación del puerto de ofertas contra Postgres.

    Recibe la fábrica de sesiones en el constructor en vez de importarla, para
    que las pruebas puedan inyectar una contra SQLite en memoria.
    """

    def __init__(self, session_factory):
        self._session_factory = session_factory

    @staticmethod
    def _a_dominio(fila: OfferModel) -> Offer:
        """Traduce una fila de la tabla al modelo de dominio."""
        return Offer(
            id=fila.id,
            postId=fila.postId,
            userId=fila.userId,
            description=fila.description,
            size=PackageSize(fila.size),
            fragile=fila.fragile,
            offer=fila.offer,
            createdAt=fila.createdAt,
        )

    def create(self, offer: Offer) -> Offer:
        """Persiste una oferta nueva y devuelve la versión con id y fecha."""
        fila = OfferModel(
            id=str(uuid.uuid4()),
            postId=offer.postId,
            userId=offer.userId,
            description=offer.description,
            size=offer.size.value,
            fragile=offer.fragile,
            offer=offer.offer,
            createdAt=utcnow(),
        )
        with self._session_factory() as session:
            session.add(fila)
            session.commit()
            session.refresh(fila)
            return self._a_dominio(fila)

    def get_by_id(self, offer_id: str) -> Optional[Offer]:
        """Obtiene una oferta por su id, o None si no existe."""
        with self._session_factory() as session:
            fila = session.get(OfferModel, offer_id)
            return self._a_dominio(fila) if fila else None

    def find(
        self, post_id: Optional[str] = None, owner_id: Optional[str] = None
    ) -> list[Offer]:
        """Lista ofertas filtrando por publicación y/o dueño, combinando con AND."""
        with self._session_factory() as session:
            consulta = session.query(OfferModel)
            if post_id is not None:
                consulta = consulta.filter(OfferModel.postId == post_id)
            if owner_id is not None:
                consulta = consulta.filter(OfferModel.userId == owner_id)
            return [self._a_dominio(fila) for fila in consulta.all()]

    def delete(self, offer_id: str) -> None:
        """Elimina una oferta existente. No falla si ya no está."""
        with self._session_factory() as session:
            fila = session.get(OfferModel, offer_id)
            if fila is not None:
                session.delete(fila)
                session.commit()

    def count(self) -> int:
        """Cuenta cuántas ofertas hay almacenadas."""
        with self._session_factory() as session:
            return session.query(OfferModel).count()

    def delete_all(self) -> None:
        """Elimina todas las ofertas."""
        with self._session_factory() as session:
            session.query(OfferModel).delete()
            session.commit()
