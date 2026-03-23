from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Fiado(Base):
    __tablename__ = "fiados"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    monto_original = Column(Float, nullable=False)
    monto_pendiente = Column(Float, nullable=False)
    descripcion = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    cliente = relationship("Cliente", back_populates="fiados")
    pagos = relationship("Pago", back_populates="fiado", cascade="all, delete-orphan")

    @property
    def esta_saldado(self) -> bool:
        return self.monto_pendiente <= 0
