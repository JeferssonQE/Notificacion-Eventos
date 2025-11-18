from pydantic import BaseModel
from datetime import datetime, date


class DolarBase(BaseModel):
    origen: str
    fecha: date
    precio_venta: float
    precio_compra: float
    diferencia_ayer: float = None


class DolarCreate(DolarBase):
    pass


class DolarOut(DolarBase):
    id: int
    scraped_at: datetime

    class Config:
        orm_mode = True
