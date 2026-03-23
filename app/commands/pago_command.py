import re
from sqlalchemy.orm import Session
from app.commands.base import Command
from app.services.fiado_service import FiadoService
from app.models.pago import MetodoPago


class PagoCommand(Command):
    """
    Maneja: #pago: nombre monto [efectivo|mp]
    Ejemplo: #pago: carlitos 1000
    Ejemplo: #pago: carlitos 1000 mp
    """

    PATTERN = re.compile(
        r"#pago\s*:\s*([a-záéíóúñ\s]+)\s+(\d+(?:\.\d+)?)(?:\s+(efectivo|mp|mercadopago))?",
        re.IGNORECASE
    )

    def can_handle(self, text: str) -> bool:
        return bool(self.PATTERN.match(text.strip()))

    def execute(self, text: str, db: Session) -> str:
        match = self.PATTERN.match(text.strip())
        if not match:
            return "❌ Formato inválido. Usá: #pago: nombre monto [efectivo|mp]"

        nombre = match.group(1).strip()
        monto = float(match.group(2))
        metodo_raw = (match.group(3) or "efectivo").lower()
        metodo = MetodoPago.MERCADOPAGO if metodo_raw in ("mp", "mercadopago") else MetodoPago.EFECTIVO

        service = FiadoService(db)
        resultado = service.registrar_pago(nombre, monto, metodo)
        return resultado.mensaje
