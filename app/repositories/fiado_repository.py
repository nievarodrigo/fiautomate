from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.fiado import Fiado
from app.repositories.base import BaseRepository


class FiadoRepository(BaseRepository[Fiado]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, id: int) -> Optional[Fiado]:
        return self.db.query(Fiado).filter(Fiado.id == id).first()

    def get_all(self) -> List[Fiado]:
        return self.db.query(Fiado).all()

    def get_pendientes(self) -> List[Fiado]:
        return self.db.query(Fiado).filter(Fiado.monto_pendiente > 0).all()

    def get_by_cliente(self, cliente_id: int) -> List[Fiado]:
        return self.db.query(Fiado).filter(
            Fiado.cliente_id == cliente_id
        ).order_by(Fiado.created_at.desc()).all()

    def get_pendientes_by_cliente(self, cliente_id: int) -> List[Fiado]:
        return self.db.query(Fiado).filter(
            Fiado.cliente_id == cliente_id,
            Fiado.monto_pendiente > 0
        ).all()

    def create(self, cliente_id: int, monto: float, descripcion: str = None) -> Fiado:
        fiado = Fiado(
            cliente_id=cliente_id,
            monto_original=monto,
            monto_pendiente=monto,
            descripcion=descripcion,
        )
        return self.save(fiado)

    def aplicar_pago(self, fiado: Fiado, monto: float) -> Fiado:
        fiado.monto_pendiente = max(0, fiado.monto_pendiente - monto)
        return self.save(fiado)

    def delete(self, id: int) -> bool:
        fiado = self.get_by_id(id)
        if not fiado:
            return False
        self.db.delete(fiado)
        self.db.commit()
        return True
