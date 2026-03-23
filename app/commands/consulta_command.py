import re
from sqlalchemy.orm import Session
from app.commands.base import Command
from app.services.fiado_service import FiadoService


class ResumenCommand(Command):
    """Maneja: #fiados → muestra resumen general de deudas."""

    def can_handle(self, text: str) -> bool:
        return text.strip().lower() == "#fiados"

    def execute(self, text: str, db: Session) -> str:
        return FiadoService(db).get_resumen_general()


class HistorialClienteCommand(Command):
    """
    Maneja: #nombre → muestra historial del cliente.
    Ejemplo: #carlitos
    """

    PATTERN = re.compile(r"#([a-záéíóúñ]+)$", re.IGNORECASE)

    def can_handle(self, text: str) -> bool:
        t = text.strip().lower()
        return bool(self.PATTERN.match(t)) and t not in ("#fiados",)

    def execute(self, text: str, db: Session) -> str:
        match = self.PATTERN.match(text.strip())
        nombre = match.group(1)
        return FiadoService(db).get_historial_cliente(nombre)
