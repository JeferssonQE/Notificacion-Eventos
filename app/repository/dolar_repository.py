from sqlalchemy.orm import Session
from app.db.models import Dolar
from app.schemas.dolar import DolarCreate
from datetime import date


class DolarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, dolar_id: int):
        return self.db.query(Dolar).filter(Dolar.id == dolar_id).first()

    def get_by_fecha(self, fecha: date):
        return self.db.query(Dolar).filter(Dolar.fecha == fecha).all()

    def get_by_origen(self, origen: str):
        return self.db.query(Dolar).filter(Dolar.origen == origen).all()

    def get_latest_by_origen(self, origen: str):
        return (
            self.db.query(Dolar)
            .filter(Dolar.origen == origen)
            .order_by(Dolar.fecha.desc())
            .first()
        )

    def get_all(self):
        return self.db.query(Dolar).all()

    def get_latest_all_origins(self):
        # Obtener el último registro de cada origen
        subquery = (
            self.db.query(
                Dolar.origen, self.db.func.max(Dolar.fecha).label("max_fecha")
            )
            .group_by(Dolar.origen)
            .subquery()
        )

        return (
            self.db.query(Dolar)
            .join(
                subquery,
                (Dolar.origen == subquery.c.origen)
                & (Dolar.fecha == subquery.c.max_fecha),
            )
            .all()
        )

    def create(
        self,
        origen: str,
        fecha: date,
        precio_venta: float,
        precio_compra: float,
        diferencia_ayer: float = None,
    ):
        dolar = Dolar(
            origen=origen,
            fecha=fecha,
            precio_venta=precio_venta,
            precio_compra=precio_compra,
            diferencia_ayer=diferencia_ayer,
        )
        self.db.add(dolar)
        self.db.commit()
        self.db.refresh(dolar)
        return dolar

    def update(
        self,
        dolar_id: int,
        origen: str = None,
        fecha: date = None,
        precio_venta: float = None,
        precio_compra: float = None,
        diferencia_ayer: float = None,
    ):
        dolar = self.get_by_id(dolar_id)
        if not dolar:
            return None

        if origen is not None:
            dolar.origen = origen
        if fecha is not None:
            dolar.fecha = fecha
        if precio_venta is not None:
            dolar.precio_venta = precio_venta
        if precio_compra is not None:
            dolar.precio_compra = precio_compra
        if diferencia_ayer is not None:
            dolar.diferencia_ayer = diferencia_ayer

        self.db.commit()
        self.db.refresh(dolar)
        return dolar

    def delete(self, dolar_id: int):
        dolar = self.get_by_id(dolar_id)
        if not dolar:
            return None

        self.db.delete(dolar)
        self.db.commit()
        return dolar
