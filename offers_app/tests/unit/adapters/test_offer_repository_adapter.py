import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from adapters.postgres.models import Base
from adapters.postgres.offer_repository_adapter import PostgresOfferRepositoryAdapter
from domain.models.offer import Offer, PackageSize


@pytest.fixture
def adaptador():
    """Adaptador real contra SQLite en memoria.

    Esta prueba ejercita el SQL de verdad —  el mapeo de columnas, los filtros,
    el commit — sin necesitar una Postgres viva. Es posible porque el adaptador
    recibe la fábrica de sesiones por constructor en vez de importarla.

    `StaticPool` mantiene una sola conexión: sin él, cada sesión abriría una
    base en memoria distinta y la tabla creada aquí no existiría en la
    siguiente consulta.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield PostgresOfferRepositoryAdapter(sessionmaker(bind=engine))
    Base.metadata.drop_all(engine)


def nueva_oferta(post_id=None, user_id=None) -> Offer:
    return Offer(
        postId=post_id or str(uuid.uuid4()),
        userId=user_id or str(uuid.uuid4()),
        description="Caja de libros",
        size=PackageSize.MEDIUM,
        fragile=False,
        offer=25.5,
    )


class TestCreate:
    def test_asigna_id_y_fecha(self, adaptador):
        guardada = adaptador.create(nueva_oferta())
        assert guardada.id is not None
        assert guardada.createdAt is not None

    def test_conserva_todos_los_campos(self, adaptador):
        original = nueva_oferta()
        guardada = adaptador.create(original)
        assert guardada.postId == original.postId
        assert guardada.userId == original.userId
        assert guardada.description == original.description
        assert guardada.size == PackageSize.MEDIUM
        assert guardada.fragile is False
        assert guardada.offer == 25.5

    def test_cada_oferta_recibe_un_id_distinto(self, adaptador):
        ids = {adaptador.create(nueva_oferta()).id for _ in range(3)}
        assert len(ids) == 3


class TestGetById:
    def test_devuelve_la_oferta_guardada(self, adaptador):
        guardada = adaptador.create(nueva_oferta())
        assert adaptador.get_by_id(guardada.id).id == guardada.id

    def test_devuelve_none_cuando_no_existe(self, adaptador):
        assert adaptador.get_by_id(str(uuid.uuid4())) is None


class TestFind:
    @pytest.fixture
    def con_datos(self, adaptador):
        post, user = str(uuid.uuid4()), str(uuid.uuid4())
        a = adaptador.create(nueva_oferta(post_id=post, user_id=user))
        b = adaptador.create(nueva_oferta(post_id=post))
        c = adaptador.create(nueva_oferta(user_id=user))
        return adaptador, post, user, a, b, c

    def test_sin_filtros_devuelve_todo(self, con_datos):
        adaptador = con_datos[0]
        assert len(adaptador.find()) == 3

    def test_filtra_por_publicacion(self, con_datos):
        adaptador, post = con_datos[0], con_datos[1]
        assert len(adaptador.find(post_id=post)) == 2

    def test_filtra_por_dueno(self, con_datos):
        adaptador, user = con_datos[0], con_datos[2]
        assert len(adaptador.find(owner_id=user)) == 2

    def test_combina_los_filtros_con_and(self, con_datos):
        adaptador, post, user, esperada, _, _ = con_datos
        encontradas = adaptador.find(post_id=post, owner_id=user)
        # Cada filtro por separado encuentra dos ofertas; cruzados, solo una.
        assert [o.id for o in encontradas] == [esperada.id]

    def test_devuelve_vacio_cuando_nada_coincide(self, adaptador):
        assert adaptador.find(post_id=str(uuid.uuid4())) == []


class TestDeleteCountYDeleteAll:
    def test_elimina_la_oferta(self, adaptador):
        guardada = adaptador.create(nueva_oferta())
        adaptador.delete(guardada.id)
        assert adaptador.get_by_id(guardada.id) is None

    def test_eliminar_algo_inexistente_no_falla(self, adaptador):
        adaptador.delete(str(uuid.uuid4()))
        assert adaptador.count() == 0

    def test_cuenta_las_ofertas(self, adaptador):
        assert adaptador.count() == 0
        adaptador.create(nueva_oferta())
        adaptador.create(nueva_oferta())
        assert adaptador.count() == 2

    def test_delete_all_vacia_la_tabla(self, adaptador):
        adaptador.create(nueva_oferta())
        adaptador.delete_all()
        assert adaptador.count() == 0
