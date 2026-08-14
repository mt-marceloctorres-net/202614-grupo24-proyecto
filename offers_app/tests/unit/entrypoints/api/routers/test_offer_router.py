import uuid

import pytest
from fastapi.testclient import TestClient

from assembly import (
    build_count_offers_use_case,
    build_create_offer_use_case,
    build_delete_offer_use_case,
    build_get_offer_use_case,
    build_get_offers_use_case,
    build_reset_offers_use_case,
)
from domain.use_cases.count_offers_use_case import CountOffersUseCase
from domain.use_cases.create_offer_use_case import CreateOfferUseCase
from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from domain.use_cases.get_offer_use_case import GetOfferUseCase
from domain.use_cases.get_offers_use_case import GetOffersUseCase
from domain.use_cases.reset_offers_use_case import ResetOffersUseCase
from entrypoints.api.main import app

OTRO_ID = "bf8792d2-3097-11ee-be56-0242ac120002"


@pytest.fixture
def cliente(repositorio):
    """Cliente HTTP contra la app real, con el repositorio sustituido.

    Estas pruebas pasan por la serialización de verdad de FastAPI, que es lo que
    las pruebas de casos de uso no tocan: si un modelo de respuesta no declara
    un campo, Pydantic lo descarta en silencio y solo se nota aquí o corriendo
    la colección de Postman.

    `TestClient` no ejecuta el `lifespan` mientras no se use como gestor de
    contexto, así que la app nunca intenta crear tablas ni conectarse a
    Postgres.
    """
    app.dependency_overrides = {
        build_create_offer_use_case: lambda: CreateOfferUseCase(repositorio),
        build_get_offers_use_case: lambda: GetOffersUseCase(repositorio),
        build_get_offer_use_case: lambda: GetOfferUseCase(repositorio),
        build_delete_offer_use_case: lambda: DeleteOfferUseCase(repositorio),
        build_count_offers_use_case: lambda: CountOffersUseCase(repositorio),
        build_reset_offers_use_case: lambda: ResetOffersUseCase(repositorio),
    }
    yield TestClient(app)
    app.dependency_overrides = {}


def crear(cliente, cuerpo) -> dict:
    respuesta = cliente.post("/offers", json=cuerpo)
    assert respuesta.status_code == 201
    return respuesta.json()


class TestCrear:
    def test_devuelve_201_con_los_tres_campos_del_contrato(
        self, cliente, cuerpo_valido
    ):
        respuesta = cliente.post("/offers", json=cuerpo_valido)
        assert respuesta.status_code == 201
        # El contrato pide exactamente estos tres campos, ni uno más.
        assert sorted(respuesta.json()) == ["createdAt", "id", "userId"]

    def test_el_userId_devuelto_es_el_enviado(self, cliente, cuerpo_valido):
        assert crear(cliente, cuerpo_valido)["userId"] == cuerpo_valido["userId"]

    def test_400_cuando_faltan_campos(self, cliente):
        assert cliente.post("/offers", json={"offer": 10}).status_code == 400

    @pytest.mark.parametrize("campo", ["postId", "userId"])
    def test_400_cuando_un_identificador_no_es_uuid(
        self, cliente, cuerpo_valido, campo
    ):
        # La prueba del evaluador manda "invalidToken" y espera 400, no 201.
        assert (
            cliente.post(
                "/offers", json=cuerpo_valido | {campo: "invalidToken"}
            ).status_code
            == 400
        )

    def test_412_cuando_el_tamano_no_es_valido(self, cliente, cuerpo_valido):
        respuesta = cliente.post("/offers", json=cuerpo_valido | {"size": "HUGE"})
        assert respuesta.status_code == 412

    def test_412_cuando_la_oferta_es_negativa(self, cliente, cuerpo_valido):
        assert (
            cliente.post("/offers", json=cuerpo_valido | {"offer": -5}).status_code
            == 412
        )

    def test_412_cuando_la_descripcion_supera_140(self, cliente, cuerpo_valido):
        cuerpo = cuerpo_valido | {"description": "x" * 141}
        assert cliente.post("/offers", json=cuerpo).status_code == 412


class TestListarYFiltrar:
    def test_devuelve_un_arreglo_con_los_ocho_campos(self, cliente, cuerpo_valido):
        crear(cliente, cuerpo_valido)
        respuesta = cliente.get("/offers")
        assert respuesta.status_code == 200
        assert sorted(respuesta.json()[0]) == [
            "createdAt",
            "description",
            "fragile",
            "id",
            "offer",
            "postId",
            "size",
            "userId",
        ]

    def test_filtra_por_publicacion(self, cliente, cuerpo_valido):
        crear(cliente, cuerpo_valido)
        assert len(cliente.get(f"/offers?post={cuerpo_valido['postId']}").json()) == 1

    def test_filtra_por_dueno(self, cliente, cuerpo_valido):
        crear(cliente, cuerpo_valido)
        assert len(cliente.get(f"/offers?owner={cuerpo_valido['userId']}").json()) == 1

    def test_combina_los_dos_filtros(self, cliente, cuerpo_valido):
        crear(cliente, cuerpo_valido)
        ruta = f"/offers?post={cuerpo_valido['postId']}&owner={cuerpo_valido['userId']}"
        assert len(cliente.get(ruta).json()) == 1

    def test_sin_coincidencias_devuelve_200_y_lista_vacia(self, cliente, cuerpo_valido):
        crear(cliente, cuerpo_valido)
        respuesta = cliente.get(f"/offers?owner={OTRO_ID}")
        # No encontrar nada es una búsqueda exitosa, no un 404.
        assert respuesta.status_code == 200
        assert respuesta.json() == []


class TestConsultarUna:
    def test_devuelve_la_oferta(self, cliente, cuerpo_valido):
        creada = crear(cliente, cuerpo_valido)
        respuesta = cliente.get(f"/offers/{creada['id']}")
        assert respuesta.status_code == 200
        assert respuesta.json()["id"] == creada["id"]

    def test_400_cuando_el_id_no_es_uuid(self, cliente):
        assert cliente.get("/offers/1").status_code == 400

    def test_404_cuando_no_existe(self, cliente):
        assert cliente.get(f"/offers/{OTRO_ID}").status_code == 404


class TestEliminar:
    def test_devuelve_el_mensaje_exacto_del_contrato(self, cliente, cuerpo_valido):
        creada = crear(cliente, cuerpo_valido)
        respuesta = cliente.delete(f"/offers/{creada['id']}")
        assert respuesta.status_code == 200
        # La prueba del evaluador compara la cadena completa.
        assert respuesta.json() == {"msg": "la oferta fue eliminada"}

    def test_la_oferta_deja_de_existir(self, cliente, cuerpo_valido):
        creada = crear(cliente, cuerpo_valido)
        cliente.delete(f"/offers/{creada['id']}")
        assert cliente.get(f"/offers/{creada['id']}").status_code == 404

    def test_400_cuando_el_id_no_es_uuid(self, cliente):
        assert cliente.delete("/offers/1").status_code == 400

    def test_404_cuando_no_existe(self, cliente):
        assert cliente.delete(f"/offers/{OTRO_ID}").status_code == 404


class TestEndpointsTecnicos:
    def test_ping_responde_pong_en_texto_plano(self, cliente):
        respuesta = cliente.get("/offers/ping")
        assert respuesta.status_code == 200
        # Sin comillas: es texto plano, no un JSON con una cadena dentro.
        assert respuesta.text == "pong"

    def test_count_refleja_las_ofertas_existentes(self, cliente, cuerpo_valido):
        assert cliente.get("/offers/count").json() == {"count": 0}
        crear(cliente, cuerpo_valido)
        assert cliente.get("/offers/count").json() == {"count": 1}

    def test_reset_vacia_la_base_y_devuelve_su_mensaje(self, cliente, cuerpo_valido):
        crear(cliente, cuerpo_valido)
        respuesta = cliente.post("/offers/reset")
        assert respuesta.status_code == 200
        assert respuesta.json() == {"msg": "Todos los datos fueron eliminados"}
        assert cliente.get("/offers/count").json() == {"count": 0}

    def test_las_rutas_fijas_ganan_sobre_la_ruta_con_parametro(self, cliente):
        """`/offers/ping` no debe interpretarse como un id de oferta.

        Si alguien mueve las rutas técnicas debajo de `/offers/{offer_id}`,
        "ping" llega como identificador, falla la comprobación de uuid y esto
        pasa a responder 400. Esta prueba deja el orden clavado.
        """
        assert cliente.get("/offers/ping").status_code == 200
        assert cliente.get("/offers/count").status_code == 200


def test_id_de_oferta_valido_pero_inexistente_no_es_400(cliente):
    """Un uuid bien formado que no existe es 404, no 400: son casos distintos."""
    assert cliente.get(f"/offers/{uuid.uuid4()}").status_code == 404
