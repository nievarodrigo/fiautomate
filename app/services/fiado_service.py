from dataclasses import dataclass
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.fiado_repository import FiadoRepository
from app.repositories.pago_repository import PagoRepository
from app.models.pago import MetodoPago


@dataclass
class ResumenCliente:
    nombre: str
    total_pendiente: float
    cantidad_fiados: int


@dataclass
class ResultadoPago:
    exito: bool
    mensaje: str
    monto_aplicado: float = 0
    monto_restante: float = 0


class FiadoService:
    def __init__(self, db: Session):
        self.db = db
        self.clientes = ClienteRepository(db)
        self.fiados = FiadoRepository(db)
        self.pagos = PagoRepository(db)

    def registrar_fiado(self, nombre: str, monto: float, descripcion: str = None) -> str:
        cliente, creado = self.clientes.get_or_create(nombre)
        fiado = self.fiados.create(cliente.id, monto, descripcion)
        return (
            f"✅ Fiado registrado\n"
            f"👤 {cliente.nombre}\n"
            f"💰 ${monto:,.0f}\n"
            f"📋 Total pendiente: ${self._total_pendiente(cliente.id):,.0f}"
        )

    def registrar_pago(self, nombre: str, monto: float, metodo: str = MetodoPago.EFECTIVO,
                       mp_payment_id: str = None) -> ResultadoPago:
        cliente = self.clientes.get_by_nombre(nombre)
        if not cliente:
            return ResultadoPago(False, f"❌ No encontré a {nombre.title()} en los fiados")

        pendientes = self.fiados.get_pendientes_by_cliente(cliente.id)
        if not pendientes:
            return ResultadoPago(False, f"✅ {cliente.nombre} no tiene deudas pendientes")

        restante = monto
        for fiado in pendientes:
            if restante <= 0:
                break
            a_aplicar = min(restante, fiado.monto_pendiente)
            self.fiados.aplicar_pago(fiado, a_aplicar)
            self.pagos.create(fiado.id, a_aplicar, metodo, mp_payment_id)
            restante -= a_aplicar

        total_aun_pendiente = self._total_pendiente(cliente.id)
        return ResultadoPago(
            exito=True,
            mensaje=(
                f"✅ Pago registrado\n"
                f"👤 {cliente.nombre}\n"
                f"💰 Pagó: ${monto:,.0f} ({metodo})\n"
                f"📋 Pendiente: ${total_aun_pendiente:,.0f}"
            ),
            monto_aplicado=monto - restante,
            monto_restante=total_aun_pendiente,
        )

    def get_resumen_general(self) -> str:
        pendientes = self.fiados.get_pendientes()
        if not pendientes:
            return "🎉 No hay fiados pendientes"

        resumen: dict[str, float] = {}
        for fiado in pendientes:
            nombre = fiado.cliente.nombre
            resumen[nombre] = resumen.get(nombre, 0) + fiado.monto_pendiente

        total_general = sum(resumen.values())
        lineas = [f"📋 *Fiados pendientes* ({len(resumen)} clientes)\n"]
        for nombre, monto in sorted(resumen.items()):
            lineas.append(f"• {nombre}: ${monto:,.0f}")
        lineas.append(f"\n💰 *Total: ${total_general:,.0f}*")
        return "\n".join(lineas)

    def get_historial_cliente(self, nombre: str) -> str:
        cliente = self.clientes.get_by_nombre(nombre)
        if not cliente:
            return f"❌ No encontré a {nombre.title()}"

        fiados = self.fiados.get_by_cliente(cliente.id)
        if not fiados:
            return f"✅ {cliente.nombre} no tiene fiados registrados"

        total_pendiente = self._total_pendiente(cliente.id)
        lineas = [f"👤 *{cliente.nombre}*\n"]
        for f in fiados:
            estado = "✅" if f.esta_saldado else "⏳"
            lineas.append(
                f"{estado} ${f.monto_original:,.0f} → debe ${f.monto_pendiente:,.0f}"
                + (f" ({f.descripcion})" if f.descripcion else "")
            )
        lineas.append(f"\n💰 *Total pendiente: ${total_pendiente:,.0f}*")
        return "\n".join(lineas)

    def procesar_pago_mercadopago(self, mp_payment_id: str, monto: float, descripcion: str) -> Optional[str]:
        if self.pagos.get_by_mp_payment_id(mp_payment_id):
            return None  # ya procesado

        nombre = self._extraer_nombre_de_descripcion(descripcion)
        if not nombre:
            return None

        resultado = self.registrar_pago(nombre, monto, MetodoPago.MERCADOPAGO, mp_payment_id)
        return resultado.mensaje if resultado.exito else None

    def _total_pendiente(self, cliente_id: int) -> float:
        return sum(f.monto_pendiente for f in self.fiados.get_pendientes_by_cliente(cliente_id))

    def _extraer_nombre_de_descripcion(self, descripcion: str) -> Optional[str]:
        if not descripcion:
            return None
        clientes = self.clientes.get_all()
        desc_lower = descripcion.lower()
        for cliente in clientes:
            if cliente.nombre.lower() in desc_lower:
                return cliente.nombre
        return None
