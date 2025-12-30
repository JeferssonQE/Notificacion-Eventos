# 🎯 Roadmap: De Pipeline ETL a Proyecto de Data Completo

## Estado Actual ✅

Tu proyecto **DólarBot** es un pipeline ETL funcional con:
- ✅ Extracción automatizada (SUNAT API + Web Scraping)
- ✅ Transformación básica (top 3, arbitraje, variaciones)
- ✅ Carga a base de datos (Supabase)
- ✅ Notificaciones (Gmail)
- ✅ Orquestación simple (GitHub Actions)

## Gaps Identificados ❌

### 1. Análisis y Visualización
- ❌ No hay dashboards interactivos
- ❌ No hay gráficos de tendencias
- ❌ No hay análisis exploratorio de datos (EDA)

### 2. Data Warehouse
- ❌ Modelo de datos plano (no dimensional)
- ❌ No hay agregaciones pre-calculadas
- ❌ No hay particionamiento optimizado

### 3. Machine Learning
- ❌ No hay modelos predictivos
- ❌ No hay detección de anomalías
- ❌ No hay forecasting

### 4. Data Quality
- ❌ No hay tests de calidad de datos
- ❌ No hay validación de schemas
- ❌ No hay monitoreo de data drift

### 5. Observabilidad
- ❌ Logs no estructurados
- ❌ No hay métricas de pipeline
- ❌ No hay alertas de fallos

---

## 🚀 Plan de Mejora (Priorizado)

### Fase 1: Analytics Básico (1-2 semanas)
**Objetivo**: Agregar capacidades de análisis y visualización

#### 1.1 Dashboard con Streamlit
```python
# app/dashboard/main.py
import streamlit as st
import plotly.express as px
from app.db.supabase.config import supabase

st.title("📊 DólarBot Analytics")

# Gráfico de tendencia histórica
df = get_historical_data()
fig = px.line(df, x='fecha', y='precio_compra', color='origen')
st.plotly_chart(fig)

# Métricas clave
col1, col2, col3 = st.columns(3)
col1.metric("Precio Actual", f"S/ {precio_actual}")
col2.metric("Variación Diaria", f"{variacion}%", delta=variacion)
col3.metric("Mejor Casa", mejor_casa)
```

**Entregables**:
- [ ] Dashboard con gráficos de tendencias
- [ ] Comparación entre casas de cambio
- [ ] Análisis de spread (diferencia compra-venta)
- [ ] Heatmap de mejores horarios/días

#### 1.2 Reportes Analíticos
```python
# app/analytics/reports.py
def generar_reporte_semanal():
    """Genera reporte con insights semanales"""
    return {
        "promedio_semanal": calcular_promedio(),
        "volatilidad": calcular_volatilidad(),
        "mejor_dia_compra": encontrar_mejor_dia(),
        "oportunidades_arbitraje": contar_arbitrajes()
    }
```

**Entregables**:
- [ ] Reporte semanal automatizado
- [ ] Análisis de volatilidad
- [ ] Identificación de patrones
- [ ] Exportación a Excel/PDF

---

### Fase 2: Data Warehouse (2-3 semanas)
**Objetivo**: Modelar datos para análisis eficiente

#### 2.1 Modelo Dimensional (Star Schema)
```sql
-- Tabla de hechos
CREATE TABLE fact_tipo_cambio (
    id SERIAL PRIMARY KEY,
    fecha_key INT REFERENCES dim_fecha(fecha_key),
    casa_key INT REFERENCES dim_casa_cambio(casa_key),
    precio_compra DECIMAL(10,4),
    precio_venta DECIMAL(10,4),
    spread DECIMAL(10,4),
    volumen_estimado INT
);

-- Dimensión Fecha
CREATE TABLE dim_fecha (
    fecha_key INT PRIMARY KEY,
    fecha DATE,
    dia_semana VARCHAR(10),
    mes VARCHAR(10),
    trimestre INT,
    es_feriado BOOLEAN
);

-- Dimensión Casa de Cambio
CREATE TABLE dim_casa_cambio (
    casa_key INT PRIMARY KEY,
    nombre VARCHAR(100),
    url VARCHAR(255),
    tipo VARCHAR(50), -- 'online', 'fisica', 'banco'
    distrito VARCHAR(100)
);
```

#### 2.2 Agregaciones Pre-calculadas
```sql
-- Vista materializada para análisis rápido
CREATE MATERIALIZED VIEW mv_resumen_diario AS
SELECT 
    fecha,
    AVG(precio_compra) as promedio_compra,
    AVG(precio_venta) as promedio_venta,
    MAX(precio_compra) as max_compra,
    MIN(precio_venta) as min_venta,
    STDDEV(precio_compra) as volatilidad
FROM fact_tipo_cambio
GROUP BY fecha;

-- Refrescar cada noche
REFRESH MATERIALIZED VIEW mv_resumen_diario;
```

**Entregables**:
- [ ] Modelo dimensional implementado
- [ ] Vistas materializadas para queries rápidas
- [ ] Particionamiento por fecha
- [ ] Índices optimizados

---

### Fase 3: Machine Learning (3-4 semanas)
**Objetivo**: Agregar capacidades predictivas

#### 3.1 Forecasting de Tipo de Cambio
```python
# app/ml/forecasting.py
from prophet import Prophet
import pandas as pd

def predecir_proximos_7_dias():
    """Predice tipo de cambio para próximos 7 días"""
    df = get_historical_data()
    df = df.rename(columns={'fecha': 'ds', 'precio_compra': 'y'})
    
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    model.fit(df)
    
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7)
```

#### 3.2 Detección de Anomalías
```python
# app/ml/anomaly_detection.py
from sklearn.ensemble import IsolationForest

def detectar_anomalias():
    """Detecta precios anómalos"""
    df = get_historical_data()
    
    model = IsolationForest(contamination=0.05)
    df['anomalia'] = model.fit_predict(df[['precio_compra', 'precio_venta']])
    
    anomalias = df[df['anomalia'] == -1]
    return anomalias
```

**Entregables**:
- [ ] Modelo de forecasting (Prophet/ARIMA)
- [ ] Detección de anomalías
- [ ] Feature engineering (lags, rolling averages)
- [ ] Model retraining automático
- [ ] API endpoint para predicciones

---

### Fase 4: Data Quality & Observability (2 semanas)
**Objetivo**: Garantizar calidad y monitoreo

#### 4.1 Tests de Calidad de Datos
```python
# app/data_quality/tests.py
from great_expectations import DataContext

def validar_datos_diarios():
    """Valida calidad de datos extraídos"""
    context = DataContext()
    
    expectations = {
        "precio_compra": {
            "min": 3.0,
            "max": 5.0,
            "not_null": True
        },
        "precio_venta": {
            "min": 3.0,
            "max": 5.0,
            "not_null": True
        },
        "spread": {
            "min": 0.0,
            "max": 0.5
        }
    }
    
    results = context.run_validation(expectations)
    
    if not results.success:
        send_alert("❌ Datos inválidos detectados")
    
    return results
```

#### 4.2 Monitoreo y Alertas
```python
# app/monitoring/metrics.py
from prometheus_client import Counter, Histogram

# Métricas
scraping_success = Counter('scraping_success_total', 'Scraping exitosos')
scraping_duration = Histogram('scraping_duration_seconds', 'Duración del scraping')
data_quality_score = Gauge('data_quality_score', 'Score de calidad de datos')

def monitor_pipeline():
    """Monitorea ejecución del pipeline"""
    with scraping_duration.time():
        try:
            data = extract_data()
            scraping_success.inc()
            
            quality_score = validate_data(data)
            data_quality_score.set(quality_score)
            
        except Exception as e:
            send_alert(f"❌ Pipeline falló: {e}")
```

**Entregables**:
- [ ] Tests de calidad con Great Expectations
- [ ] Validación de schemas con Pydantic
- [ ] Monitoreo con Prometheus/Grafana
- [ ] Alertas en Slack/Discord
- [ ] Logs estructurados (JSON)

---

### Fase 5: Orquestación Avanzada (2 semanas)
**Objetivo**: Pipeline robusto y escalable

#### 5.1 Migrar a Airflow
```python
# dags/dolar_etl_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True
}

with DAG(
    'dolar_etl',
    default_args=default_args,
    schedule_interval='0 13 * * *',  # 1 PM diario
    catchup=False
) as dag:
    
    extract_sunat = PythonOperator(
        task_id='extract_sunat',
        python_callable=extract_sunat_data
    )
    
    extract_casas = PythonOperator(
        task_id='extract_casas',
        python_callable=extract_casas_data
    )
    
    validate_data = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data_quality
    )
    
    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data
    )
    
    load_warehouse = PythonOperator(
        task_id='load_warehouse',
        python_callable=load_to_warehouse
    )
    
    train_model = PythonOperator(
        task_id='train_model',
        python_callable=retrain_ml_model,
        trigger_rule='all_success'
    )
    
    send_report = PythonOperator(
        task_id='send_report',
        python_callable=send_daily_report
    )
    
    # Dependencias
    [extract_sunat, extract_casas] >> validate_data >> transform >> load_warehouse
    load_warehouse >> [train_model, send_report]
```

**Entregables**:
- [ ] DAG de Airflow con dependencias
- [ ] Backfilling de datos históricos
- [ ] Retry policies configurables
- [ ] Monitoreo de SLA
- [ ] Documentación de tareas

---

## 📊 Arquitectura Objetivo

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                       │
│                    (Airflow / Prefect)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Extract    │  │  Transform   │  │     Load     │
│              │  │              │  │              │
│ • SUNAT API  │  │ • Validation │  │ • Data Lake  │
│ • Scraping   │  │ • Enrichment │  │ • Warehouse  │
│ • Validation │  │ • ML Features│  │ • Cache      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Data Quality │  │  ML Models   │  │  Analytics   │
│              │  │              │  │              │
│ • Tests      │  │ • Forecasting│  │ • Dashboard  │
│ • Monitoring │  │ • Anomalies  │  │ • Reports    │
│ • Alerts     │  │ • Retraining │  │ • API        │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🎯 Priorización Recomendada

### Quick Wins (1-2 semanas)
1. **Dashboard con Streamlit** - Impacto visual inmediato
2. **Reportes semanales** - Más insights sin mucho esfuerzo
3. **Tests de calidad básicos** - Previene errores

### Medium Term (1-2 meses)
4. **Data Warehouse** - Base para análisis avanzado
5. **ML Forecasting** - Diferenciador clave
6. **Monitoreo robusto** - Confiabilidad

### Long Term (3+ meses)
7. **Airflow** - Escalabilidad
8. **Feature Store** - ML en producción
9. **Real-time streaming** - Datos en tiempo real

---

## 📚 Stack Tecnológico Recomendado

### Analytics & Visualization
- **Streamlit** - Dashboard interactivo
- **Plotly/Altair** - Gráficos interactivos
- **Pandas/Polars** - Manipulación de datos

### Data Warehouse
- **dbt** - Transformaciones SQL
- **Supabase/PostgreSQL** - Storage (ya lo tienes)
- **Particionamiento** - Optimización

### Machine Learning
- **Prophet** - Forecasting de series temporales
- **scikit-learn** - Modelos clásicos
- **MLflow** - Tracking de experimentos

### Data Quality
- **Great Expectations** - Tests de calidad
- **Pydantic** - Validación de schemas
- **pytest** - Tests unitarios

### Orchestration
- **Airflow** - Orquestación compleja
- **Prefect** - Alternativa moderna
- **GitHub Actions** - Simple (ya lo tienes)

### Monitoring
- **Prometheus + Grafana** - Métricas
- **Sentry** - Error tracking
- **Loguru** - Logs estructurados

---

## 💡 Recursos de Aprendizaje

### Cursos
- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp)

### Libros
- "Fundamentals of Data Engineering" - Joe Reis
- "Designing Data-Intensive Applications" - Martin Kleppmann

### Proyectos de Referencia
- [Awesome Data Engineering](https://github.com/igorbarinov/awesome-data-engineering)
- [Data Engineering Projects](https://github.com/topics/data-engineering-project)

---

## ✅ Checklist de Proyecto de Data Completo

### ETL/ELT
- [x] Extracción automatizada
- [x] Transformación básica
- [x] Carga a base de datos
- [ ] Orquestación avanzada (Airflow)
- [ ] Backfilling de datos históricos

### Data Warehouse
- [ ] Modelo dimensional (star schema)
- [ ] Vistas materializadas
- [ ] Particionamiento
- [ ] Índices optimizados

### Analytics
- [ ] Dashboard interactivo
- [ ] Reportes automatizados
- [ ] KPIs calculados
- [ ] Análisis exploratorio

### Machine Learning
- [ ] Modelo de forecasting
- [ ] Detección de anomalías
- [ ] Feature engineering
- [ ] Model retraining automático

### Data Quality
- [ ] Tests de calidad
- [ ] Validación de schemas
- [ ] Monitoreo de drift
- [ ] Alertas automáticas

### Observability
- [ ] Logs estructurados
- [ ] Métricas de pipeline
- [ ] Dashboards de monitoreo
- [ ] Alertas de fallos

### Documentation
- [ ] Documentación de datos (data catalog)
- [ ] Lineage de datos
- [ ] Runbooks
- [ ] Architecture Decision Records (ADRs)

---

**Última actualización**: Diciembre 2024
