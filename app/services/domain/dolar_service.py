from sqlalchemy.orm import Session
from app.repository.dolar_repository import DolarRepository
from app.schemas.dolar import DolarCreate
from datetime import date


class DolarService:
    def __init__(self, db: Session):
        self.repo = DolarRepository(db)

    def listar_todos_dolares(self):
        return self.repo.get_all()

    def listar_dolares_por_fecha(self, fecha: date):
        return self.repo.get_by_fecha(fecha)

    def listar_dolares_por_origen(self, origen: str):
        return self.repo.get_by_origen(origen)

    def obtener_ultimo_dolar_por_origen(self, origen: str):
        dolar = self.repo.get_latest_by_origen(origen)
        if not dolar:
            raise ValueError(
                f"No se encontraron datos de dólar para el origen: {origen}"
            )
        return dolar

    def obtener_ultimos_dolares_todos_origenes(self):
        return self.repo.get_latest_all_origins()

    def obtener_dolar(self, dolar_id: int):
        dolar = self.repo.get_by_id(dolar_id)
        if not dolar:
            raise ValueError("Dólar no encontrado")
        return dolar

    def crear_dolar(self, data: DolarCreate):
        # Validaciones adicionales
        if not data.origen:
            raise ValueError("El origen es obligatorio")
        if not data.fecha:
            raise ValueError("La fecha es obligatoria")
        if data.precio_venta <= 0:
            raise ValueError("El precio de venta debe ser mayor a 0")
        if data.precio_compra <= 0:
            raise ValueError("El precio de compra debe ser mayor a 0")

        return self.repo.create(
            origen=data.origen,
            fecha=data.fecha,
            precio_venta=data.precio_venta,
            precio_compra=data.precio_compra,
            diferencia_ayer=data.diferencia_ayer,
        )

    def actualizar_dolar(self, dolar_id: int, data: DolarCreate):
        dolar = self.repo.update(
            dolar_id=dolar_id,
            origen=data.origen,
            fecha=data.fecha,
            precio_venta=data.precio_venta,
            precio_compra=data.precio_compra,
            diferencia_ayer=data.diferencia_ayer,
        )
        if not dolar:
            raise ValueError("Dólar no encontrado")
        return dolar

    def borrar_dolar(self, dolar_id: int):
        dolar = self.repo.delete(dolar_id)
        if not dolar:
            raise ValueError("Dólar no encontrado o ya eliminado")
        return dolar
