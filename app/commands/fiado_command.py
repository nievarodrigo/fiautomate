import re
from sqlalchemy.orm import Session
from app.commands.base import Command
from app.services.fiado_service import FiadoService


class FiadoCommand(Command):
    """
    Maneja: #fiado: nombre monto, nombre2 monto2, ...
    Ejemplo: #fiado: carlitos 2000, pepecabeza 1200
    """

    PATTERN = re.compile(r"#fiado[s]?\s*:\s*(.+)", re.IGNORECASE)
    ITEM_PATTERN = re.compile(r"([a-záéíóúñ\s]+)\s+(\d+(?:\.\d+)?)", re.IGNORECASE)

    def can_handle(self, text: str) -> bool:
        return bool(self.PATTERN.match(text.strip()))

    def execute(self, text: str, db: Session) -> str:
        match = self.PATTERN.match(text.strip())
        if not match:
            return "❌ Formato inválido. Usá: #fiado: nombre monto, nombre2 monto2"

        contenido = match.group(1)
        items = self.ITEM_PATTERN.findall(contenido)

        if not items:
            return "❌ No entendí los datos. Ejemplo: #fiado: carlitos 2000, pepecabeza 1200"

        service = FiadoService(db)
        respuestas = []
        for nombre, monto in items:
            respuesta = service.registrar_fiado(nombre.strip(), float(monto))
            respuestas.append(respuesta)

        return "\n\n".join(respuestas)
