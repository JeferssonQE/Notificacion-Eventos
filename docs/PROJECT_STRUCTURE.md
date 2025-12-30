# 📁 Estructura del Proyecto

## Estructura Actual (Limpia - Data Pipeline)

```
dolar/
├── .github/
│   └── workflows/
│       └── daily.yml              # Orquestación con GitHub Actions
│
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuración centralizada (Pydantic)
│   │
│   ├── scraper/                   # ETL - Extract
│   │   ├── __init__.py
│   │   ├── get_sunat_dolar.py     # Extracción API SUNAT
│   │   ├── top_3_cambio.py        # Scraping casas de cambio
│   │   ├── scraper_dolar.py       # Scraper alternativo
│   │   ├── scraper_selenium.py    # Scraper con Selenium
│   │   └── scraper.py             # Scraper base
│   │
│   ├── services/                  # ETL - Transform & Load
│   │   ├── infrastructure/
│   │   │   ├── gmail/
│   │   │   │   ├── mailer.py      # Servicio de notificaciones
│   │   │   │   └── reporte_casas.html  # Template HTML
│   │   │   └── test_gmail.py      # Script principal ETL
│   │   └── __init__.py
│   │
│   ├── db/                        # Data Warehouse
│   │   ├── supabase/
│   │   │   ├── config.py          # Cliente Supabase
│   │   │   └── __init__.py
│   │   ├── models/                # Modelos de datos
│   │   ├── migrations/            # Migraciones SQL
│   │   ├── database.py
│   │   └── __init__.py
│   │
│   ├── dashboard/                 # Analytics UI
│   │   └── main.py                # Dashboard Streamlit
│   │
│   └── __init__.py
│
├── tests/
│   ├── test_scraper.py            # Tests de extracción
│   └── test_alerta.py             # Tests de alertas
│
├── .env.example                   # Template de variables de entorno
├── .gitignore
├── ARCHITECTURE.md                # Documentación de arquitectura
├── DATA_ROADMAP.md                # Plan de mejoras
├── LICENSE
├── README.md
├── requirements.txt               # Dependencias Python
└── SETUP.md                       # Guía de configuración
```

## Componentes Principales

### 1. ETL Pipeline (`app/scraper/` + `app/services/`)

**Extract**:
- `get_sunat_dolar.py`: Extrae tipo de cambio oficial de SUNAT API
- `top_3_cambio.py`: Scraping de 15+ casas de cambio

**Transform**:
- Cálculo de variaciones porcentuales
- Identificación de top 3 mejores tasas
- Detección de arbitraje

**Load**:
- `test_gmail.py`: Orquesta el pipeline completo
- Persiste en Supabase
- Envía notificaciones por Gmail

### 2. Data Warehouse (`app/db/`)

**Supabase (PostgreSQL)**:
- Tabla `dolar`: Histórico de tipos de cambio
- Índices optimizados para queries
- Validación de duplicados

### 3. Analytics (`app/dashboard/`)

**Streamlit Dashboard**:
- Visualización de tendencias
- Análisis de spread
- Métricas en tiempo real

### 4. Orchestration (`.github/workflows/`)

**GitHub Actions**:
- Ejecución diaria automática (13:00 Lima)
- Manejo de secrets
- Logs de ejecución

## Archivos Eliminados (Innecesarios para Data Pipeline)

```
❌ Eliminados:
├── docker-compose.yml             # No se usa Docker en producción
├── Dockerfile                     # No se usa Docker en producción
├── app/main.py                    # API REST no necesaria
├── app/api/                       # Endpoints REST no necesarios
├── app/schemas/                   # Schemas de API no necesarios
├── app/repository/                # Capa de repositorio redundante
├── app/celery/                    # Celery no necesario (GitHub Actions)
├── app/cache/                     # Redis no necesario
├── app/utils/                     # Utilidades no usadas
├── app/deployment/                # Deployment configs no usadas
├── app/services/domain/           # Servicios de dominio no necesarios
├── app/services/infrastructure/whatsapp/  # WhatsApp no implementado
├── celerybeat-schedule.*          # Archivos de Celery
├── notifi.zip                     # Archivo temporal
└── ideas.txt                      # Notas personales
```

## Dependencias Actuales

### Core ETL
- `beautifulsoup4` - Web scraping
- `selenium` - Automatización de navegador
- `requests` - HTTP client
- `pydantic` - Validación de datos
- `python-dotenv` - Variables de entorno

### Data Warehouse
- `supabase` - Cliente PostgreSQL
- `SQLAlchemy` - ORM

### Analytics
- `pandas` - Manipulación de datos
- `plotly` - Visualizaciones
- `streamlit` - Dashboard

### Data Quality
- `great-expectations` - Tests de calidad

## Próximos Pasos

Ver [DATA_ROADMAP.md](./DATA_ROADMAP.md) para el plan completo de mejoras.

### Quick Wins
1. Completar dashboard de Streamlit
2. Agregar tests de calidad de datos
3. Implementar reportes semanales

### Medium Term
4. Modelo dimensional en Supabase
5. ML forecasting con Prophet
6. Monitoreo robusto

### Long Term
7. Migrar a Airflow
8. Feature store para ML
9. Real-time streaming

---

**Última actualización**: Diciembre 2024
