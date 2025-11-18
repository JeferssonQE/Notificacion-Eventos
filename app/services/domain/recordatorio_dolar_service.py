from sqlalchemy.orm import Session
from app.repository.recordatorio_dolar_repository import RecordatorioDolarRepository
from app.schemas.recordatorio_dolar import RecordatorioDolarCreate


class RecordatorioDolarService:
    def __init__(self, db: Session):
        self.repo = RecordatorioDolarRepository(db)

    def listar_recordatorios_por_numero(self, numero: str):
        return self.repo.get_by_numero(numero)

    def listar_todos_recordatorios(self):
        return self.repo.get_all()

    def obtener_recordatorio(self, recordatorio_id: int):
        recordatorio = self.repo.get_by_id(recordatorio_id)
        if not recordatorio:
            raise ValueError("Recordatorio no encontrado")
        return recordatorio

    def crear_recordatorio(self, data: RecordatorioDolarCreate):
        # Validaciones adicionales
        if not data.numero:
            raise ValueError("El número es obligatorio")
        if not data.nombre:
            raise ValueError("El nombre es obligatorio")
        if not data.movimiento:
            raise ValueError("El movimiento es obligatorio")
        if not data.porcentaje:
            raise ValueError("El porcentaje es obligatorio")
        if not data.valor:
            raise ValueError("El valor es obligatorio")

        return self.repo.create(
            numero=data.numero,
            nombre=data.nombre,
            movimiento=data.movimiento,
            porcentaje=data.porcentaje,
            valor=data.valor,
        )

    def actualizar_recordatorio(
        self, recordatorio_id: int, data: RecordatorioDolarCreate
    ):
        recordatorio = self.repo.update(
            recordatorio_id=recordatorio_id,
            numero=data.numero,
            nombre=data.nombre,
            movimiento=data.movimiento,
            porcentaje=data.porcentaje,
            valor=data.valor,
        )
        if not recordatorio:
            raise ValueError("Recordatorio no encontrado")
        return recordatorio

    def borrar_recordatorio(self, recordatorio_id: int):
        recordatorio = self.repo.delete(recordatorio_id)
        if not recordatorio:
            raise ValueError("Recordatorio no encontrado o ya eliminado")
        return recordatorio
