import uuid

import pytest

from domain.models.offer import Offer
from domain.use_cases.count_offers_use_case import CountOffersUseCase
from domain.use_cases.create_offer_use_case import CreateOfferUseCase
from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from domain.use_cases.get_offer_use_case import GetOfferUseCase
from domain.use_cases.get_offers_use_case import GetOffersUseCase
from domain.use_cases.reset_offers_use_case import ResetOffersUseCase
from errors import InvalidOfferValueError, OfferNotFoundError


class TestCreateOfferUseCase:
    def test_persiste_y_devuelve_la_oferta_con_id_y_fecha(
        self, repositorio, datos_validos
    ):
        oferta = CreateOfferUseCase(repositorio).execute(datos_validos)
        assert oferta.id is not None and oferta.createdAt is not None
        assert repositorio.count() == 1

    def test_no_persiste_cuando_la_regla_de_negocio_falla(
        self, repositorio, datos_validos
    ):
        datos = datos_validos.model_copy(update={"offer": -1})
        with pytest.raises(InvalidOfferValueError):
            CreateOfferUseCase(repositorio).execute(datos)
        # Lo que importa no es la excepción sino que la base quede intacta.
        assert repositorio.count() == 0


class TestGetOffersUseCase:
    @pytest.fixture
    def con_dos_ofertas(self, repositorio, datos_validos):
        primera = CreateOfferUseCase(repositorio).execute(datos_validos)
        otros = datos_validos.model_copy(
            update={"postId": str(uuid.uuid4()), "userId": str(uuid.uuid4())}
        )
        segunda = CreateOfferUseCase(repositorio).execute(otros)
        return repositorio, primera, segunda

    def test_sin_filtros_devuelve_todas(self, con_dos_ofertas):
        repo, _, _ = con_dos_ofertas
        assert len(GetOffersUseCase(repo).execute()) == 2

    def test_filtra_por_publicacion(self, con_dos_ofertas):
        repo, primera, _ = con_dos_ofertas
        assert GetOffersUseCase(repo).execute(post_id=primera.postId) == [primera]

    def test_filtra_por_dueno(self, con_dos_ofertas):
        repo, _, segunda = con_dos_ofertas
        assert GetOffersUseCase(repo).execute(owner_id=segunda.userId) == [segunda]

    def test_combina_los_filtros_con_and(self, con_dos_ofertas):
        repo, primera, segunda = con_dos_ofertas
        # Cada filtro por separado encuentra una oferta, pero cruzados no hay
        # ninguna: si el repositorio los combinara con OR, esto devolvería dos.
        assert (
            GetOffersUseCase(repo).execute(
                post_id=primera.postId, owner_id=segunda.userId
            )
            == []
        )

    def test_una_busqueda_sin_resultados_no_es_un_error(self, repositorio):
        assert GetOffersUseCase(repositorio).execute(post_id=str(uuid.uuid4())) == []


class TestGetOfferUseCase:
    def test_devuelve_la_oferta(self, repositorio, datos_validos):
        creada = CreateOfferUseCase(repositorio).execute(datos_validos)
        assert GetOfferUseCase(repositorio).execute(creada.id) == creada

    def test_falla_cuando_no_existe(self, repositorio):
        with pytest.raises(OfferNotFoundError):
            GetOfferUseCase(repositorio).execute(str(uuid.uuid4()))


class TestDeleteOfferUseCase:
    def test_elimina_la_oferta(self, repositorio, datos_validos):
        creada = CreateOfferUseCase(repositorio).execute(datos_validos)
        DeleteOfferUseCase(repositorio).execute(creada.id)
        assert repositorio.count() == 0

    def test_falla_cuando_no_existe(self, repositorio):
        # El adaptador borra en silencio cuando el id no está; el caso de uso
        # tiene que distinguirlo porque el contrato exige 404.
        with pytest.raises(OfferNotFoundError):
            DeleteOfferUseCase(repositorio).execute(str(uuid.uuid4()))


class TestCountYReset:
    def test_cuenta_las_ofertas(self, repositorio, datos_validos):
        assert CountOffersUseCase(repositorio).execute() == 0
        CreateOfferUseCase(repositorio).execute(datos_validos)
        assert CountOffersUseCase(repositorio).execute() == 1

    def test_reset_vacia_la_tabla(self, repositorio, datos_validos):
        CreateOfferUseCase(repositorio).execute(datos_validos)
        ResetOffersUseCase(repositorio).execute()
        assert CountOffersUseCase(repositorio).execute() == 0

    def test_reset_sobre_una_base_vacia_no_falla(self, repositorio):
        ResetOffersUseCase(repositorio).execute()
        assert CountOffersUseCase(repositorio).execute() == 0


def test_el_modelo_de_dominio_no_depende_del_repositorio():
    """Una oferta se puede construir sin tocar ningún adaptador."""
    oferta = Offer(
        postId=str(uuid.uuid4()),
        userId=str(uuid.uuid4()),
        description="Sin repositorio",
        size="SMALL",
        fragile=True,
        offer=1.0,
    )
    assert oferta.fragile is True
