from abc import ABC, abstractmethod


class BaseUseCase(ABC):
    """Clase base de los casos de uso."""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Ejecuta el caso de uso."""
        pass
