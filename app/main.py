# FastAPI entry point - Data Analytics API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.api.v1.dolar import router as dolar_router

app = FastAPI(
    title="Dólar Analytics API",
    description="API para análisis de datos del tipo de cambio del dólar en Perú",
    version="2.0.0",
)

# CORS para permitir acceso desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta básica
@app.get("/")
def root():
    return {
        "message": "Dólar Analytics API",
        "version": "2.0.0",
        "docs": "/docs",
        "features": [
            "Datos históricos BCRP",
            "Datos de mercado internacional (Cobre, DXY)",
            "Análisis de casas de cambio",
            "Métricas de volatilidad y spread",
            "Detección de arbitraje"
        ]
    }

# Health checks
app.include_router(health_router, prefix="/api", tags=["health"])

# API v1 - Data Analytics
app.include_router(dolar_router, prefix="/api/v1", tags=["dolar"])
