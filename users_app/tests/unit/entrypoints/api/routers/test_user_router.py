from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from entrypoints.api.routers import user_router as user_router_module
from errors import (
    InvalidCredentialsError,
    InvalidRequestError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class FakeUseCase:
    """Doble de prueba: envuelve una función como si fuera un caso de uso."""

    def __init__(self, fn):
        self._fn = fn

    def execute(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


@pytest.fixture
def app():
    fastapi_app = FastAPI()
    fastapi_app.include_router(user_router_module.router)
    return fastapi_app


@pytest.fixture
def client(app):
    return TestClient(app)


def override(app, dependency, fn):
    app.dependency_overrides[dependency] = lambda: FakeUseCase(fn)


def test_create_user_success(app, client):
    def fake_create(**kwargs):
        return type("U", (), {"id": "abc", "createdAt": datetime(2026, 1, 1)})()

    override(app, user_router_module.build_create_user_use_case, fake_create)

    response = client.post(
        "/users", json={"username": "jdoe", "password": "p", "email": "j@example.com"}
    )

    assert response.status_code == 201
    assert response.json()["id"] == "abc"


def test_create_user_conflict(app, client):
    def fake_create(**kwargs):
        raise UserAlreadyExistsError("ya existe")

    override(app, user_router_module.build_create_user_use_case, fake_create)

    response = client.post(
        "/users", json={"username": "jdoe", "password": "p", "email": "j@example.com"}
    )

    assert response.status_code == 412


def test_update_user_success(app, client):
    override(app, user_router_module.build_update_user_use_case, lambda **kwargs: None)

    response = client.patch("/users/abc", json={"fullName": "Nuevo"})

    assert response.status_code == 200


def test_update_user_without_fields(app, client):
    def fake_update(**kwargs):
        raise InvalidRequestError("nada que actualizar")

    override(app, user_router_module.build_update_user_use_case, fake_update)

    response = client.patch("/users/abc", json={})

    assert response.status_code == 400


def test_update_user_not_found(app, client):
    def fake_update(**kwargs):
        raise UserNotFoundError("no existe")

    override(app, user_router_module.build_update_user_use_case, fake_update)

    response = client.patch("/users/no-existe", json={"fullName": "X"})

    assert response.status_code == 404


def test_authenticate_success(app, client):
    def fake_auth(**kwargs):
        return type(
            "U", (), {"id": "abc", "token": "tok", "expireAt": datetime(2026, 1, 1)}
        )()

    override(app, user_router_module.build_authenticate_user_use_case, fake_auth)

    response = client.post("/users/auth", json={"username": "jdoe", "password": "p"})

    assert response.status_code == 200
    assert response.json()["token"] == "tok"


def test_authenticate_invalid_credentials(app, client):
    def fake_auth(**kwargs):
        raise InvalidCredentialsError("credenciales inválidas")

    override(app, user_router_module.build_authenticate_user_use_case, fake_auth)

    response = client.post("/users/auth", json={"username": "jdoe", "password": "mala"})

    assert response.status_code == 404


def test_get_me_success(app, client):
    from domain.models.user import UserStatus

    def fake_get_me(**kwargs):
        return type(
            "U",
            (),
            {
                "id": "abc",
                "username": "jdoe",
                "email": "j@example.com",
                "fullName": None,
                "dni": None,
                "phoneNumber": None,
                "status": UserStatus.POR_VERIFICAR,
            },
        )()

    override(app, user_router_module.build_get_me_use_case, fake_get_me)

    response = client.get("/users/me", headers={"Authorization": "Bearer tok"})

    assert response.status_code == 200
    assert response.json()["username"] == "jdoe"


def test_get_me_invalid_token(app, client):
    def fake_get_me(**kwargs):
        raise InvalidTokenError("token inválido")

    override(app, user_router_module.build_get_me_use_case, fake_get_me)

    response = client.get("/users/me", headers={"Authorization": "Bearer malo"})

    assert response.status_code == 401


def test_get_me_without_header(client):
    response = client.get("/users/me")

    assert response.status_code == 403


def test_count_users(app, client):
    override(app, user_router_module.build_count_users_use_case, lambda: 3)

    response = client.get("/users/count")

    assert response.status_code == 200
    assert response.json()["count"] == 3


def test_ping(client):
    response = client.get("/users/ping")

    assert response.status_code == 200
    assert response.text == "pong"


def test_reset_users(app, client):
    override(app, user_router_module.build_reset_users_use_case, lambda: None)

    response = client.post("/users/reset")

    assert response.status_code == 200
