# app/schemas/recordatorio_dolar.py

from pydantic import BaseModel
from datetime import datetime


class RecordatorioDolarBase(BaseModel):
    numero: str
    nombre: str
    movimiento: str
    porcentaje: str
    valor: str


class RecordatorioDolarCreate(RecordatorioDolarBase):
    pass


class RecordatorioDolarOut(RecordatorioDolarBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
