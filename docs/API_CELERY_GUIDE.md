# 🚀 API REST y Celery - Guía de Uso

## Descripción

Este proyecto ahora incluye:
- **API REST** con FastAPI para consultar datos y analytics
- **Celery** para tareas asíncronas (scraping, análisis, reportes)
- **Redis** como broker de mensajes para Celery

## 📋 Requisitos

```bash
pip install fastapi uvicorn celery redis
```

## 🔧 Configuración

### 1. Instalar Redis

**Windows:**
```bash
# Usar Docker
docker run -d -p 6379:6379 redis:alpine

# O instalar desde: https://github.com/microsoftarchive/redis/releases
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# Mac
brew install redis
```

### 2. Configurar .env

Agrega a tu archivo `.env`:
```env
REDIS_URL=redis://localhost:6379/0
```

## 🚀 Ejecutar la API

### Desarrollo
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Accede a:
- **API**: http://localhost:8000
- **Docs interactivos**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Endpoints Disponibles

### Casas de Cambio

```bash
# Precios más recientes
GET /api/v1/casas/latest

# Historial de una casa específica
GET /api/v1/casas/history/{casa_name}?days=7

# Analytics de todas las casas
GET /api/v1/casas/analytics?days=7

# Oportunidades de trading y arbitraje
GET /api/v1/casas/opportunities
```

### BCRP (Banco Central)

```bash
# Datos más recientes
GET /api/v1/bcrp/latest

# Historial
GET /api/v1/bcrp/history?start_date=2024-01-01&end_date=2024-12-31&limit=30
```

### Market (Cobre, DXY)

```bash
# Datos más recientes
GET /api/v1/market/latest

# Historial
GET /api/v1/market/history?start_date=2024-01-01&limit=30
```

### Dashboard

```bash
# Resumen completo para dashboard
GET /api/v1/dashboard/summary
```

## 🔄 Ejecutar Celery

### Worker (procesa tareas)
```bash
celery -A app.celery.config worker --loglevel=info --pool=solo
```

### Beat (scheduler para tareas periódicas)
```bash
celery -A app.celery.config beat --loglevel=info
```

### Flower (monitoreo web de Celery)
```bash
pip install flower
celery -A app.celery.config flower --port=5555
```
Accede a: http://localhost:5555

## 📝 Tareas Celery Disponibles

### Scraping
```python
# Scrapear casas de cambio
from app.celery.task import scrape_hourly_casas
result = scrape_hourly_casas.delay()

# Ingestar datos diarios (BCRP + Market)
from app.celery.task import ingest_daily_data
result = ingest_daily_data.delay()
```

### Analytics
```python
# Calcular analytics
from app.celery.task import calculate_analytics
result = calculate_analytics.delay(days=7)

# Detectar arbitraje
from app.celery.task import detect_arbitrage
result = detect_arbitrage.delay()
```

### Reportes
```python
# Generar reporte diario
from app.celery.task import generate_daily_report
result = generate_daily_report.delay()

# Resumen semanal
from app.celery.task import generate_weekly_summary
result = generate_weekly_summary.delay()
```

### Mantenimiento
```python
# Limpiar datos antiguos
from app.celery.task import cleanup_old_data
result = cleanup_old_data.delay(days_to_keep=90)

# Health check
from app.celery.task import health_check
result = health_check.delay()
```

## 🐳 Docker (Opcional)

Crea un `docker-compose.yml`:

```yaml
version: '3.8'

services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - redis
  
  celery_worker:
    build: .
    command: celery -A app.celery.config worker --loglevel=info
    env_file:
      - .env
    depends_on:
      - redis
  
  celery_beat:
    build: .
    command: celery -A app.celery.config beat --loglevel=info
    env_file:
      - .env
    depends_on:
      - redis
```

Ejecutar:
```bash
docker-compose up -d
```

## 🧪 Probar la API

### Con curl
```bash
# Health check
curl http://localhost:8000/api/health

# Últimos precios
curl http://localhost:8000/api/v1/casas/latest

# Analytics
curl http://localhost:8000/api/v1/casas/analytics?days=7

# Dashboard completo
curl http://localhost:8000/api/v1/dashboard/summary
```

### Con Python
```python
import requests

# Obtener oportunidades
response = requests.get("http://localhost:8000/api/v1/casas/opportunities")
data = response.json()
print(data)
```

## 📈 Beneficios para tu CV

Con esta implementación puedes demostrar:

✅ **Arquitectura de microservicios** con FastAPI  
✅ **Procesamiento asíncrono** con Celery  
✅ **Message broker** con Redis  
✅ **API REST** bien documentada (OpenAPI/Swagger)  
✅ **Containerización** con Docker  
✅ **Data pipeline** completo (ETL + Analytics)  
✅ **Monitoreo** con Flower  
✅ **Buenas prácticas** (separación de concerns, DRY, SOLID)

## 🔗 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Celery Docs](https://docs.celeryq.dev/)
- [Redis Docs](https://redis.io/docs/)
- [Docker Docs](https://docs.docker.com/)
