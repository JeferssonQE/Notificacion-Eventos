# 📖 Documentación Técnica - Dólar Analytics Platform

## Índice

1. [Arquitectura](#arquitectura)
2. [API REST](#api-rest)
3. [Celery Tasks](#celery-tasks)
4. [Pipeline ETL](#pipeline-etl)
5. [Base de Datos](#base-de-datos)
6. [Workflows](#workflows)
7. [Configuración](#configuración)
8. [Deployment](#deployment)

---

## Arquitectura

### Componentes Principales

```
┌──────────────────────────────────────────────────────────┐
│                   GitHub Actions                          │
│  ┌─────────────────┐      ┌──────────────────┐          │
│  │ Daily Workflow  │      │ Hourly Workflow  │          │
│  │ (1:00 PM Lima)  │      │ (4x al día)      │          │
│  └────────┬────────┘      └────────┬─────────┘          │
└───────────┼──────────────────────────┼───────────────────┘
            │                          │
            ▼                          ▼
┌───────────────────────────────────────────────────────────┐
│                    ETL Pipeline                            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐    │
│  │   Extract    │→ │  Transform   │→ │    Load     │    │
│  │ BCRP+Market  │  │  Analytics   │  │  Supabase   │    │
│  │ Casas Cambio │  │  Arbitraje   │  │  + Email    │    │
│  └──────────────┘  └──────────────┘  └─────────────┘    │
└───────────────────────────────────────────────────────────┘
            │                          │
            ▼                          ▼
┌─────────────────────┐    ┌──────────────────────────┐
│    FastAPI Server   │    │   Celery Workers         │
│  ┌───────────────┐  │    │  ┌────────────────────┐ │
│  │ REST API      │  │    │  │ Scraping Tasks     │ │
│  │ /api/v1/...   │  │    │  │ Analytics Tasks    │ │
│  │ /docs         │  │    │  │ Report Tasks       │ │
│  └───────────────┘  │    │  └────────────────────┘ │
└──────────┬──────────┘    └───────────┬──────────────┘
           │                           │
           └───────────┬───────────────┘
                       ▼
           ┌───────────────────────┐
           │   Redis (Broker)      │
           └───────────────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │  Supabase (PostgreSQL)│
           │  ┌─────────────────┐  │
           │  │ bcrp_data       │  │
           │  │ market_data     │  │
           │  │ dolar_hourly    │  │
           │  └─────────────────┘  │
           └───────────────────────┘
```

### Stack Tecnológico

- **Backend**: Python 3.11, FastAPI, Celery
- **Data Engineering**: Pandas, yfinance, BeautifulSoup, Selenium
- **Storage**: Supabase (PostgreSQL)
- **Message Broker**: Redis
- **CI/CD**: GitHub Actions
- **Monitoring**: Flower (Celery), Health checks

---

## API REST

### Iniciar Servidor

```bash
# Desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Endpoints

#### Health Checks
```bash
GET /api/health              # Estado general
GET /api/health/db           # Estado de Supabase
GET /api/health/celery       # Estado de Celery
```

#### Casas de Cambio
```bash
GET /api/v1/casas/latest                    # Precios más recientes
GET /api/v1/casas/history/{casa}?days=7     # Historial por casa
GET /api/v1/casas/analytics?days=7          # Métricas estratégicas
GET /api/v1/casas/opportunities             # Arbitraje
```

#### BCRP
```bash
GET /api/v1/bcrp/latest                     # Último dato
GET /api/v1/bcrp/history?start_date=2024-01-01&limit=30
```

#### Market (Cobre, DXY)
```bash
GET /api/v1/market/latest                   # Último dato
GET /api/v1/market/history?limit=30
```

#### Dashboard
```bash
GET /api/v1/dashboard/summary               # Resumen completo
```

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Celery Tasks

### Configuración

```bash
# Instalar Redis
docker run -d -p 6379:6379 redis:alpine

# Iniciar Worker
celery -A app.celery.config worker --loglevel=info --pool=solo

# Iniciar Beat (scheduler)
celery -A app.celery.config beat --loglevel=info

# Monitoreo con Flower
celery -A app.celery.config flower --port=5555
# http://localhost:5555
```

### Tareas Disponibles

#### Scraping
```python
from app.celery.task import scrape_hourly_casas, ingest_daily_data

# Scrapear casas de cambio
result = scrape_hourly_casas.delay()

# Ingestar datos diarios (BCRP + Market)
result = ingest_daily_data.delay()
```

#### Analytics
```python
from app.celery.task import calculate_analytics, detect_arbitrage

# Calcular métricas
result = calculate_analytics.delay(days=7)

# Detectar arbitraje
result = detect_arbitrage.delay()
```

#### Reportes
```python
from app.celery.task import generate_daily_report, generate_weekly_summary

# Reporte diario
result = generate_daily_report.delay()

# Resumen semanal
result = generate_weekly_summary.delay()
```

#### Mantenimiento
```python
from app.celery.task import cleanup_old_data, health_check

# Limpiar datos antiguos (>90 días)
result = cleanup_old_data.delay(days_to_keep=90)

# Health check
result = health_check.delay()
```

---

## Pipeline ETL

### 1. Extract (Extracción)

**Fuentes de datos:**
- API SUNAT (tipo de cambio oficial)
- API BCRP (tipo de cambio interbancario, tasa interbancaria)
- Yahoo Finance (precio cobre, índice DXY)
- Web scraping de 15+ casas de cambio

**Scripts:**
```bash
# BCRP
python -m app.services.bcrp_service

# Market
python -m app.services.market_service

# Casas de cambio
python -m app.scraper.hourly_scraper
```

### 2. Transform (Transformación)

**Métricas calculadas:**
- Volatilidad (desviación estándar)
- Spread (diferencia venta-compra)
- Variaciones (1h, 24h, 7d)
- Ranking de estabilidad
- Detección de arbitraje

**Script:**
```bash
python -m app.analytics.price_analysis
```

### 3. Load (Carga)

**Destinos:**
- Supabase (PostgreSQL)
  - `bcrp_data` - Datos diarios BCRP
  - `market_data` - Datos mercado internacional
  - `dolar_hourly` - Datos horarios casas
- Gmail (reportes HTML)

**Script:**
```bash
python -m app.services.data_ingestion
```

---

## Base de Datos

### Tablas en Supabase

#### bcrp_data
```sql
CREATE TABLE bcrp_data (
    id BIGSERIAL PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    tc_interbancario_venta DECIMAL(10, 4),
    tasa_interbancaria DECIMAL(10, 4),
    origen VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### market_data
```sql
CREATE TABLE market_data (
    id BIGSERIAL PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    precio_cobre DECIMAL(10, 4),
    indice_dxy DECIMAL(10, 4),
    origen VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### dolar_hourly
```sql
CREATE TABLE dolar_hourly (
    id BIGSERIAL PRIMARY KEY,
    origen VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    precio_compra DECIMAL(10, 4) NOT NULL,
    precio_venta DECIMAL(10, 4) NOT NULL,
    spread DECIMAL(10, 4),
    url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Migraciones

```bash
# Ejecutar migraciones
psql -h <host> -U <user> -d <db> -f app/db/migrations/create_market_data_tables.sql
psql -h <host> -U <user> -d <db> -f app/db/migrations/create_dolar_hourly_table.sql
```

---

## Workflows

### Daily Workflow

**Archivo**: `.github/workflows/daily.yml`  
**Schedule**: `0 18 * * *` (1:00 PM Lima)

**Pasos:**
1. Ingesta datos diarios (BCRP + Market)
2. Genera reporte con analytics
3. Envía email

**Ejecución manual:**
```bash
# En GitHub: Actions → Notificacion-dolar-diario → Run workflow
```

### Hourly Workflow

**Archivo**: `.github/workflows/hourly_scraping.yml`  
**Schedule**: `0 13,17,21,1 * * *` (9am, 12pm, 4pm, 8pm Lima)

**Pasos:**
1. Scrapea casas de cambio
2. Inserta en `dolar_hourly`
3. Calcula métricas

---

## Configuración

### Variables de Entorno

```env
# SUNAT API
TOKEN_SUNAT_API=your_token

# Gmail
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
EMAIL_TO=recipient@gmail.com

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_API_KEY=your_anon_key
SUPABASE_PASSWORD=your_db_password

# Redis (opcional)
REDIS_URL=redis://localhost:6379/0
```

### GitHub Secrets

Configurar en: `Settings → Secrets and variables → Actions`

- `TOKEN_SUNAT_API`
- `EMAIL_USER`
- `EMAIL_PASS`
- `EMAIL_TO`
- `SUPABASE_URL`
- `SUPABASE_API_KEY`

---

## Deployment

### Docker Compose (Recomendado)

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
```

**Ejecutar:**
```bash
docker-compose up -d
```

### Manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar .env
cp .env.example .env

# 3. Iniciar servicios
# Terminal 1: Redis
docker run -d -p 6379:6379 redis:alpine

# Terminal 2: API
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 3: Celery
celery -A app.celery.config worker --loglevel=info --pool=solo
```

---

## Testing

### API
```bash
python tests_scripts/test_api_local.py
```

### Celery
```bash
python tests_scripts/test_celery_tasks.py
```

### Analytics
```bash
python tests_scripts/test_analytics.py
```

---

## Troubleshooting

### Error: Redis connection refused
```bash
# Verificar que Redis esté corriendo
docker ps | grep redis

# Iniciar Redis
docker run -d -p 6379:6379 redis:alpine
```

### Error: Supabase connection
```bash
# Verificar credenciales en .env
# Verificar que SUPABASE_URL y SUPABASE_API_KEY sean correctos
```

### Error: Celery worker not found
```bash
# Verificar que el worker esté corriendo
celery -A app.celery.config inspect active
```

---

## Recursos Adicionales

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Celery Docs](https://docs.celeryq.dev/)
- [Supabase Docs](https://supabase.com/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## Contacto

**Jefersson Kevin Quicaña Erquinio**  
GitHub: [@Manzanito20003](https://github.com/Manzanito20003)  
Email: jefersson.quicana@utec.edu.pe
