import uuid
from datetime import datetime, timezone
from typing import Optional

import pytest

from domain.models.offer import Offer, OfferCreate, PackageSize
from domain.ports.offer_repository_port import OfferRepositoryPort


class FakeOfferRepository(OfferRepositoryPort):
    """Repositorio en memoria para probar los casos de uso.

    Implementa el mismo puerto que el adaptador de Postgres. Los casos de uso no
    notan la diferencia — de eso se trata la arquitectura hexagonal — y las
    pruebas corren sin base de datos, en milisegundos.

    Reproduce dos comportamientos del adaptador real que importan: asigna el id
    y la fecha al persistir, y `delete` no falla si el id no existe.
    """

    def __init__(self):
        self.ofertas: dict[str, Offer] = {}

    def create(self, offer: Offer) -> Offer:
        guardada = offer.model_copy(
            update={
                "id": str(uuid.uuid4()),
                "createdAt": datetime.now(timezone.utc).replace(tzinfo=None),
            }
        )
        self.ofertas[guardada.id] = guardada
        return guardada

    def get_by_id(self, offer_id: str) -> Optional[Offer]:
        return self.ofertas.get(offer_id)

    def find(
        self, post_id: Optional[str] = None, owner_id: Optional[str] = None
    ) -> list[Offer]:
        return [
            o
            for o in self.ofertas.values()
            if (post_id is None or o.postId == post_id)
            and (owner_id is None or o.userId == owner_id)
        ]

    def delete(self, offer_id: str) -> None:
        self.ofertas.pop(offer_id, None)

    def count(self) -> int:
        return len(self.ofertas)

    def delete_all(self) -> None:
        self.ofertas.clear()


@pytest.fixture
def repositorio() -> FakeOfferRepository:
    """Repositorio vacío, nuevo para cada prueba."""
    return FakeOfferRepository()


@pytest.fixture
def datos_validos() -> OfferCreate:
    """Cuerpo de creación que cumple todas las reglas del contrato."""
    return OfferCreate(
        postId=str(uuid.uuid4()),
        userId=str(uuid.uuid4()),
        description="Caja de libros",
        size=PackageSize.MEDIUM.value,
        fragile=False,
        offer=25.5,
    )


@pytest.fixture
def cuerpo_valido(datos_validos: OfferCreate) -> dict:
    """El mismo cuerpo, como diccionario, para las pruebas de router."""
    return datos_validos.model_dump()
