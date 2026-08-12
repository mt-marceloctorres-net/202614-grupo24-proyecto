from typing import Optional

import pytest

from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort


class FakeUserRepository(UserRepositoryPort):
    """Repositorio en memoria para pruebas unitarias, sin depender de Postgres."""

    def __init__(self):
        self.users: dict[str, User] = {}

    def create(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username or user.email == email:
                return user
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def get_by_token(self, token: str) -> Optional[User]:
        for user in self.users.values():
            if user.token == token:
                return user
        return None

    def update(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def count(self) -> int:
        return len(self.users)

    def delete_all(self) -> None:
        self.users.clear()


@pytest.fixture
def user_repository() -> FakeUserRepository:
    """Repositorio en memoria vacío para cada prueba."""
    return FakeUserRepository()


@pytest.fixture
def valid_user_data():
    """Datos válidos para crear un usuario."""
    return {
        "username": "jdoe",
        "password": "secret123",
        "email": "jdoe@example.com",
        "dni": "123",
        "fullName": "John Doe",
        "phoneNumber": "3001234567",
    }
