from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.repositories.base import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, id: int) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(Cliente.id == id).first()

    def get_by_nombre(self, nombre: str) -> Optional[Cliente]:
        return self.db.query(Cliente).filter(
            Cliente.nombre.ilike(nombre)
        ).first()

    def get_all(self) -> List[Cliente]:
        return self.db.query(Cliente).order_by(Cliente.nombre).all()

    def create(self, nombre: str, telefono: str = None) -> Cliente:
        cliente = Cliente(nombre=nombre.strip().title(), telefono=telefono)
        return self.save(cliente)

    def get_or_create(self, nombre: str) -> tuple[Cliente, bool]:
        cliente = self.get_by_nombre(nombre)
        if cliente:
            return cliente, False
        return self.create(nombre), True

    def delete(self, id: int) -> bool:
        cliente = self.get_by_id(id)
        if not cliente:
            return False
        self.db.delete(cliente)
        self.db.commit()
        return True
