from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class Command(ABC):
    """Clase base para todos los comandos de WhatsApp."""

    @abstractmethod
    def can_handle(self, text: str) -> bool:
        """Retorna True si este comando puede manejar el texto recibido."""
        pass

    @abstractmethod
    def execute(self, text: str, db: Session) -> str:
        """Ejecuta el comando y retorna la respuesta a enviar."""
        pass
