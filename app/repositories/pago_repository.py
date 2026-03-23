from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.pago import Pago
from app.repositories.base import BaseRepository


class PagoRepository(BaseRepository[Pago]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, id: int) -> Optional[Pago]:
        return self.db.query(Pago).filter(Pago.id == id).first()

    def get_all(self) -> List[Pago]:
        return self.db.query(Pago).order_by(Pago.created_at.desc()).all()

    def get_by_fiado(self, fiado_id: int) -> List[Pago]:
        return self.db.query(Pago).filter(Pago.fiado_id == fiado_id).all()

    def get_by_mp_payment_id(self, mp_payment_id: str) -> Optional[Pago]:
        return self.db.query(Pago).filter(Pago.mp_payment_id == mp_payment_id).first()

    def create(self, fiado_id: int, monto: float, metodo: str, mp_payment_id: str = None, nota: str = None) -> Pago:
        pago = Pago(
            fiado_id=fiado_id,
            monto=monto,
            metodo=metodo,
            mp_payment_id=mp_payment_id,
            nota=nota,
        )
        return self.save(pago)

    def delete(self, id: int) -> bool:
        pago = self.get_by_id(id)
        if not pago:
            return False
        self.db.delete(pago)
        self.db.commit()
        return True
