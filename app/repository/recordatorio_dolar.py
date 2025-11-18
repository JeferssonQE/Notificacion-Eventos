# app/db/repository/recordatorio_dolar.py

from sqlalchemy.orm import Session
from app.db.models import RecordatorioDolar
from app.schemas.recordatorio_dolar import RecordatorioDolarCreate


class RecordatorioDolarRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, data: RecordatorioDolarCreate) -> RecordatorioDolar:
        obj = RecordatorioDolar(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def obtener_por_numero(self, numero: int) -> RecordatorioDolar | None:
        return (
            self.db.query(RecordatorioDolar)
            .filter(RecordatorioDolar.numero == numero)
            .first()
        )

    def eliminar_por_id(self, id: int) -> RecordatorioDolar | None:
        obj = self.obtener_por_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

    # TODO: UPDATE BY ID

    # ---Helper---
    def obtener_por_id(self, id: int) -> RecordatorioDolar | None:
        return (
            self.db.query(RecordatorioDolar).filter(RecordatorioDolar.id == id).first()
        )
