from sqlalchemy.orm import Session
from app.repository.evento_repository import EventoRepository
from app.schemas.evento import EventoCreate


class EventoService:
    def __init__(self, db: Session):
        self.repo = EventoRepository(db)

    def listar_eventos_por_numero(self, numero: str):
        return self.repo.get_by_numero(numero)

    def obtener_evento(self, evento_id: int):
        evento = self.repo.get_by_id(evento_id)
        if not evento:
            raise ValueError("Evento no encontrado")
        return evento

    def crear_evento(self, data: EventoCreate):
        # Aquí puedes aplicar lógica adicional
        if not data.numero:
            raise ValueError("El nombre es obligatorio")
        return self.repo.create(
            data.numero, data.nombre, data.title, data.body, data.fecha, data.hora
        )

    def borrar_evento(self, evento_id: int, numero: str = None):
        evento = self.repo.delete(evento_id, numero)
        if not evento:
            raise ValueError("Evento no encontrado o ya eliminado")
        return evento
