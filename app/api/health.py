from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint para monitoreo"""
    return {
        "status": "healthy",
        "service": "Dólar Analytics API",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }


@router.get("/health/db")
def database_health():
    """Verifica conexión a Supabase"""
    try:
        from app.db.supabase.client import get_supabase_client
        
        supabase = get_supabase_client()
        # Intenta hacer una query simple
        result = supabase.table("bcrp_data").select("id").limit(1).execute()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.get("/health/celery")
def celery_health():
    """Verifica estado de Celery"""
    try:
        from app.celery.config import celery_app
        
        # Inspeccionar workers activos
        inspect = celery_app.control.inspect()
        active_workers = inspect.active()
        
        if active_workers:
            return {
                "status": "healthy",
                "celery": "running",
                "workers": list(active_workers.keys()),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "warning",
                "celery": "no_workers",
                "message": "No hay workers activos",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "celery": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
