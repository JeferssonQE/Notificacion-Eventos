from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.domain.recordatorio_dolar_service import RecordatorioDolarService
from app.schemas.recordatorio_dolar import RecordatorioDolarCreate

router = APIRouter()


@router.get("/recordatorios")
def listar_todos_recordatorios(db: Session = Depends(get_db)):
    return RecordatorioDolarService(db).listar_todos_recordatorios()


@router.get("/recordatorios/numero/{numero}")
def listar_recordatorios_por_numero(numero: str, db: Session = Depends(get_db)):
    return RecordatorioDolarService(db).listar_recordatorios_por_numero(numero)


@router.get("/recordatorios/{recordatorio_id}")
def obtener_recordatorio(recordatorio_id: int, db: Session = Depends(get_db)):
    try:
        return RecordatorioDolarService(db).obtener_recordatorio(recordatorio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/recordatorios")
def crear_recordatorio(data: RecordatorioDolarCreate, db: Session = Depends(get_db)):
    try:
        return RecordatorioDolarService(db).crear_recordatorio(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/recordatorios/{recordatorio_id}")
def actualizar_recordatorio(
    recordatorio_id: int, data: RecordatorioDolarCreate, db: Session = Depends(get_db)
):
    try:
        return RecordatorioDolarService(db).actualizar_recordatorio(
            recordatorio_id, data
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/recordatorios/{recordatorio_id}")
def borrar_recordatorio(recordatorio_id: int, db: Session = Depends(get_db)):
    try:
        return RecordatorioDolarService(db).borrar_recordatorio(recordatorio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
