from sqlalchemy.orm import Session
from app.db.models import Evento
from datetime import date, time


class EventoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Evento).all()

    def get_by_id(self, evento_id: int, numero: str = None):
        return (
            self.db.query(Evento)
            .filter(Evento.id == evento_id and Evento.numero == numero)
            .first()
        )

    def get_by_numero(self, numero: str):
        return self.db.query(Evento).filter(Evento.numero == numero).all()

    def create(self, numero: str, nombre: str, title: str, body: str, fecha, hora):
        evento = Evento(
            numero=numero,
            nombre=nombre,
            title=title,
            body=body,
            fecha=fecha,
            hora=time(hora),
        )
        self.db.add(evento)
        self.db.commit()
        self.db.refresh(evento)
        return evento

    def delete(self, evento_id: int):
        evento = self.get_by_id(evento_id)
        if evento:
            self.db.delete(evento)
            self.db.commit()
        return evento
