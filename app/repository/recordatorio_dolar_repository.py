from sqlalchemy.orm import Session
from app.db.models import RecordatorioDolar
from app.schemas.recordatorio_dolar import RecordatorioDolarCreate


class RecordatorioDolarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, recordatorio_id: int):
        return (
            self.db.query(RecordatorioDolar)
            .filter(RecordatorioDolar.id == recordatorio_id)
            .first()
        )

    def get_by_numero(self, numero: str):
        return (
            self.db.query(RecordatorioDolar)
            .filter(RecordatorioDolar.numero == numero)
            .all()
        )

    def get_all(self):
        return self.db.query(RecordatorioDolar).all()

    def create(
        self, numero: str, nombre: str, movimiento: str, porcentaje: str, valor: str
    ):
        recordatorio = RecordatorioDolar(
            numero=numero,
            nombre=nombre,
            movimiento=movimiento,
            porcentaje=porcentaje,
            valor=valor,
        )
        self.db.add(recordatorio)
        self.db.commit()
        self.db.refresh(recordatorio)
        return recordatorio

    def update(
        self,
        recordatorio_id: int,
        numero: str = None,
        nombre: str = None,
        movimiento: str = None,
        porcentaje: str = None,
        valor: str = None,
    ):
        recordatorio = self.get_by_id(recordatorio_id)
        if not recordatorio:
            return None

        if numero is not None:
            recordatorio.numero = numero
        if nombre is not None:
            recordatorio.nombre = nombre
        if movimiento is not None:
            recordatorio.movimiento = movimiento
        if porcentaje is not None:
            recordatorio.porcentaje = porcentaje
        if valor is not None:
            recordatorio.valor = valor

        self.db.commit()
        self.db.refresh(recordatorio)
        return recordatorio

    def delete(self, recordatorio_id: int):
        recordatorio = self.get_by_id(recordatorio_id)
        if not recordatorio:
            return None

        self.db.delete(recordatorio)
        self.db.commit()
        return recordatorio
