from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.domain.dolar_service import DolarService
from app.schemas.dolar import DolarCreate
from datetime import date

router = APIRouter()


@router.get("/dolares")
def listar_todos_dolares(db: Session = Depends(get_db)):
    return DolarService(db).listar_todos_dolares()


@router.get("/dolares/fecha/{fecha}")
def listar_dolares_por_fecha(fecha: date, db: Session = Depends(get_db)):
    return DolarService(db).listar_dolares_por_fecha(fecha)


@router.get("/dolares/origen/{origen}")
def listar_dolares_por_origen(origen: str, db: Session = Depends(get_db)):
    return DolarService(db).listar_dolares_por_origen(origen)


@router.get("/dolares/ultimo/{origen}")
def obtener_ultimo_dolar_por_origen(origen: str, db: Session = Depends(get_db)):
    try:
        return DolarService(db).obtener_ultimo_dolar_por_origen(origen)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/dolares/ultimos")
def obtener_ultimos_dolares_todos_origenes(db: Session = Depends(get_db)):
    return DolarService(db).obtener_ultimos_dolares_todos_origenes()


@router.get("/dolares/{dolar_id}")
def obtener_dolar(dolar_id: int, db: Session = Depends(get_db)):
    try:
        return DolarService(db).obtener_dolar(dolar_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/dolares")
def crear_dolar(data: DolarCreate, db: Session = Depends(get_db)):
    try:
        return DolarService(db).crear_dolar(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/dolares/{dolar_id}")
def actualizar_dolar(dolar_id: int, data: DolarCreate, db: Session = Depends(get_db)):
    try:
        return DolarService(db).actualizar_dolar(dolar_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/dolares/{dolar_id}")
def borrar_dolar(dolar_id: int, db: Session = Depends(get_db)):
    try:
        return DolarService(db).borrar_dolar(dolar_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
