from abc import ABC, abstractmethod
from typing import Optional

from domain.models.user import User


class UserRepositoryPort(ABC):
    """Interfaz del repositorio de usuarios."""

    @abstractmethod
    def create(self, user: User) -> User:
        """Crea un nuevo usuario."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por su id."""
        pass

    @abstractmethod
    def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        """Obtiene un usuario por username o email (para validar unicidad)."""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por su username (para autenticación)."""
        pass

    @abstractmethod
    def get_by_token(self, token: str) -> Optional[User]:
        """Obtiene un usuario por su token de sesión vigente."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario existente."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Cuenta cuántos usuarios hay almacenados."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Elimina todos los usuarios."""
        pass
