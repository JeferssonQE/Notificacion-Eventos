from pydantic import BaseModel, validator
from datetime import date, time


class EventoCreate(BaseModel):
    numero: str
    nombre: str
    title: str
    body: str
    fecha: date  # YYYY-MM-DD
    hora: time  # HH:MM

    @validator("hora", pre=True)
    def truncar_hora(cls, value):
        if isinstance(value, str):
            # Si es string tipo "22:23:33.389000"
            h, m, *_ = value.split(":")
            return time(int(h), int(m))
        elif isinstance(value, time):
            # Si ya es datetime.time con segundos
            return time(value.hour, value.minute)
        return value
