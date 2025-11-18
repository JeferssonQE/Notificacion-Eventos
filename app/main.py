# FastAPI entry point
from fastapi import FastAPI
from app.api.v1.eventos import router as api_router
from app.api.health import router as health_router
from app.api.v1.eventos import router as eventos_router
from app.api.v1.recordatorios import router as recordatorios_router
from app.api.v1.dolar import router as dolar_router

app = FastAPI(
    title="DólarBot API",
    description="API para gestión de alertas de dólar y notificaciones",
    version="1.0.0",
)


# Ruta básica de prueba
@app.get("/")
def root():
    return {"message": "DólarBot API", "version": "1.0.0", "docs": "/docs"}


# Health checks
app.include_router(health_router, prefix="/api", tags=["health"])

# API v1
app.include_router(eventos_router, prefix="/api/v1", tags=["eventos"])
app.include_router(recordatorios_router, prefix="/api/v1", tags=["recordatorios"])
app.include_router(dolar_router, prefix="/api/v1", tags=["dolar"])

# Webhook routes (mantener compatibilidad)
app.include_router(api_router, prefix="/api", tags=["webhook"])
