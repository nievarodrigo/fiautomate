from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base


class MetodoPago:
    EFECTIVO = "efectivo"
    MERCADOPAGO = "mercadopago"


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    fiado_id = Column(Integer, ForeignKey("fiados.id"), nullable=False)
    monto = Column(Float, nullable=False)
    metodo = Column(String, default=MetodoPago.EFECTIVO)
    mp_payment_id = Column(String, nullable=True, unique=True)
    nota = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    fiado = relationship("Fiado", back_populates="pagos")
