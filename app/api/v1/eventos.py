from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.domain.evento_service import EventoService
from app.schemas.evento import EventoCreate

router = APIRouter()


@router.get("/eventos")
def listar_eventos(db: Session = Depends(get_db)):
    return EventoService(db).listar_eventos()


@router.get("/eventos/{evento_id}")
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    try:
        return EventoService(db).obtener_evento(evento_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/eventos")
def crear_evento(data: EventoCreate, db: Session = Depends(get_db)):
    try:
        return EventoService(db).crear_evento(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
