from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from datetime import datetime
import psutil
import os

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check básico - verifica que la aplicación esté funcionando
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }


@router.get("/health/detailed")
def detailed_health_check(db: Session = Depends(get_db)):
    """
    Health check detallado - verifica base de datos y recursos del sistema
    """
    try:
        # Verificar conexión a la base de datos
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Información del sistema
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    disk_usage = psutil.disk_usage("/").percent

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": db_status,
        "system": {
            "memory_usage_percent": memory_usage,
            "cpu_usage_percent": cpu_usage,
            "disk_usage_percent": disk_usage,
        },
    }


@router.get("/health/ready")
def readiness_check():
    """
    Readiness check - verifica que la aplicación esté lista para recibir tráfico
    """
    return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}


@router.get("/health/live")
def liveness_check():
    """
    Liveness check - verifica que la aplicación esté viva
    """
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
