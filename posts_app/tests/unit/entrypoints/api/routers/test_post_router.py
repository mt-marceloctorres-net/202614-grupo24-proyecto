from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from entrypoints.api.main import app as real_app
from entrypoints.api.routers import post_router as post_router_module
from errors import InvalidExpirationError, PostNotFoundError


class FakeUseCase:
    """Doble de prueba: envuelve una función como si fuera un caso de uso."""

    def __init__(self, fn):
        self._fn = fn

    def execute(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


@pytest.fixture
def app():
    """La app real de `entrypoints/api/main.py`, no una copia.

    Usar la app real (en vez de construir una `FastAPI()` aparte y
    duplicar a mano sus `exception_handler`) evita que las pruebas queden
    validando una copia que puede desalinearse del código real — pasó una
    vez con el manejador de `RequestValidationError` (ver `main.py`) y no
    se detectó hasta correr el pipeline oficial.

    `TestClient` **sin usarse como context manager** (`with ... as client`)
    no dispara el `lifespan` de FastAPI, así que `Base.metadata.create_all`
    nunca se ejecuta aquí — la prueba sigue sin necesitar Postgres real.
    Se limpian los `dependency_overrides` al final porque `real_app` es un
    singleton compartido entre pruebas, a diferencia de una app nueva por
    prueba.
    """
    yield real_app
    real_app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    return TestClient(app)


def override(app, dependency, fn):
    app.dependency_overrides[dependency] = lambda: FakeUseCase(fn)


VALID_BODY = {
    "routeId": "11111111-1111-1111-1111-111111111111",
    "userId": "22222222-2222-2222-2222-222222222222",
    "expireAt": "2026-12-31T23:59:59",
}


def _fake_post(**overrides):
    data = {
        "id": "abc",
        "routeId": VALID_BODY["routeId"],
        "userId": VALID_BODY["userId"],
        "expireAt": datetime(2026, 12, 31, 23, 59, 59),
        "createdAt": datetime(2026, 1, 1),
    }
    data.update(overrides)
    return type("P", (), data)()


def test_create_post_success(app, client):
    override(
        app,
        post_router_module.build_create_post_use_case,
        lambda **kwargs: _fake_post(),
    )

    response = client.post("/posts", json=VALID_BODY)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == "abc"
    assert body["userId"] == VALID_BODY["userId"]


def test_create_post_invalid_expiration(app, client):
    def fake_create(**kwargs):
        raise InvalidExpirationError("La fecha expiración no es válida")

    override(app, post_router_module.build_create_post_use_case, fake_create)

    response = client.post("/posts", json=VALID_BODY)

    assert response.status_code == 412
    assert response.json() == {"msg": "La fecha expiración no es válida"}


def test_create_post_missing_field(client):
    incomplete_body = {"routeId": VALID_BODY["routeId"], "userId": VALID_BODY["userId"]}

    response = client.post("/posts", json=incomplete_body)

    assert response.status_code == 400


def test_create_post_invalid_route_id_format(client):
    body = {**VALID_BODY, "routeId": "invalidId"}

    response = client.post("/posts", json=body)

    assert response.status_code == 400


def test_create_post_invalid_user_id_format(client):
    body = {**VALID_BODY, "userId": "invalidId"}

    response = client.post("/posts", json=body)

    assert response.status_code == 400


def test_list_posts_without_filters(app, client):
    captured = {}

    def fake_list(**kwargs):
        captured.update(kwargs)
        return [_fake_post()]

    override(app, post_router_module.build_list_posts_use_case, fake_list)

    response = client.get("/posts")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert captured == {"expire": None, "route": None, "owner": None}


def test_list_posts_with_expire_filter(app, client):
    captured = {}

    def fake_list(**kwargs):
        captured.update(kwargs)
        return []

    override(app, post_router_module.build_list_posts_use_case, fake_list)

    response = client.get("/posts", params={"expire": "true"})

    assert response.status_code == 200
    assert captured["expire"] is True


def test_list_posts_with_route_filter(app, client):
    captured = {}

    def fake_list(**kwargs):
        captured.update(kwargs)
        return []

    override(app, post_router_module.build_list_posts_use_case, fake_list)

    response = client.get("/posts", params={"route": "r1"})

    assert response.status_code == 200
    assert captured["route"] == "r1"


def test_list_posts_with_owner_filter(app, client):
    captured = {}

    def fake_list(**kwargs):
        captured.update(kwargs)
        return []

    override(app, post_router_module.build_list_posts_use_case, fake_list)

    response = client.get("/posts", params={"owner": "u1"})

    assert response.status_code == 200
    assert captured["owner"] == "u1"


def test_list_posts_with_combined_filters(app, client):
    captured = {}

    def fake_list(**kwargs):
        captured.update(kwargs)
        return []

    override(app, post_router_module.build_list_posts_use_case, fake_list)

    response = client.get(
        "/posts", params={"expire": "false", "route": "r1", "owner": "u1"}
    )

    assert response.status_code == 200
    assert captured == {"expire": False, "route": "r1", "owner": "u1"}


def test_get_post_found(app, client):
    override(
        app, post_router_module.build_get_post_use_case, lambda **kwargs: _fake_post()
    )

    response = client.get("/posts/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 200
    assert response.json()["id"] == "abc"


def test_get_post_not_found(app, client):
    def fake_get(**kwargs):
        raise PostNotFoundError("no existe")

    override(app, post_router_module.build_get_post_use_case, fake_get)

    response = client.get("/posts/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 404


def test_get_post_invalid_uuid_format(app, client):
    def unreachable(**kwargs):
        raise AssertionError("no debería invocarse el caso de uso con un id inválido")

    override(app, post_router_module.build_get_post_use_case, unreachable)

    response = client.get("/posts/no-es-un-uuid")

    assert response.status_code == 400


def test_delete_post_success(app, client):
    override(app, post_router_module.build_delete_post_use_case, lambda **kwargs: None)

    response = client.delete("/posts/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 200
    assert response.json() == {"msg": "la publicación fue eliminada"}


def test_delete_post_not_found(app, client):
    def fake_delete(**kwargs):
        raise PostNotFoundError("no existe")

    override(app, post_router_module.build_delete_post_use_case, fake_delete)

    response = client.delete("/posts/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 404


def test_delete_post_invalid_uuid_format(app, client):
    def unreachable(**kwargs):
        raise AssertionError("no debería invocarse el caso de uso con un id inválido")

    override(app, post_router_module.build_delete_post_use_case, unreachable)

    response = client.delete("/posts/no-es-un-uuid")

    assert response.status_code == 400


def test_count_posts(app, client):
    override(app, post_router_module.build_count_posts_use_case, lambda: 5)

    response = client.get("/posts/count")

    assert response.status_code == 200
    assert response.json() == {"count": 5}


def test_ping(client):
    response = client.get("/posts/ping")

    assert response.status_code == 200
    assert response.text == "pong"


def test_reset_posts(app, client):
    override(app, post_router_module.build_reset_posts_use_case, lambda: None)

    response = client.post("/posts/reset")

    assert response.status_code == 200
    assert response.json() == {"msg": "Todos los datos fueron eliminados"}
