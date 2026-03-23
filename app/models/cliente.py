from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    fiados = relationship("Fiado", back_populates="cliente", cascade="all, delete-orphan")
