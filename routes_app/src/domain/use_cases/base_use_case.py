from abc import ABC, abstractmethod


class BaseUseCase(ABC):
    """Base interface for application use cases."""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the use case."""
