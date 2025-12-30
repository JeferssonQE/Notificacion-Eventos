# 📊 Setup de Market Data (BCRP + Yahoo Finance)

Guía para configurar e ingestar datos de mercado en tu base de datos.

## 🎯 ¿Qué datos obtendrás?

### BCRP (Banco Central de Reserva del Perú)
- **Tipo de cambio interbancario venta** (USD/PEN)
- **Tasa interbancaria** (tasa de interés en soles)

### Yahoo Finance (Mercados Internacionales)
- **Precio del Cobre** (HG=F) - Vital para Perú como exportador
- **Índice Dólar DXY** (DX-Y.NYB) - Tendencia global del USD

---

## 🚀 Pasos de Instalación

### 1. Instalar dependencias

```bash
pip install yfinance
```

O instala todo desde requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Crear las tablas en Supabase

**Opción A: Usando el script Python (recomendado)**

```bash
python setup_market_tables.py
```

**Opción B: Manualmente en Supabase**

Si el script falla, ve al SQL Editor de Supabase y ejecuta:

```sql
-- Copia y pega el contenido de:
app/db/migrations/create_market_data_tables.sql
```

### 3. Verificar que las tablas se crearon

En Supabase, deberías ver:
- ✅ `bcrp_data`
- ✅ `market_data`

---

## 💾 Ingestar Datos

### Opción 1: Últimos 30 días (recomendado para empezar)

```bash
python app/services/data_ingestion.py
```

### Opción 2: Personalizar el rango

Edita `app/services/data_ingestion.py` al final del archivo:

```python
if __name__ == "__main__":
    # Últimos 90 días
    ingest_last_days(90)
    
    # O histórico desde 2020
    # ingest_historical(2020)
    
    # O rango específico
    # ingest_data("2024-01-01", "2024-12-31")
```

---

## 📊 Estructura de las Tablas

### `bcrp_data`
```sql
- id (BIGSERIAL)
- fecha (DATE) - UNIQUE
- tc_interbancario_venta (DECIMAL)
- tasa_interbancaria (DECIMAL)
- origen (VARCHAR) - 'BCRP_API'
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
```

### `market_data`
```sql
- id (BIGSERIAL)
- fecha (DATE) - UNIQUE
- precio_cobre (DECIMAL)
- indice_dxy (DECIMAL)
- origen (VARCHAR) - 'YAHOO'
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
```

---

## 🔄 Actualización Automática

Para mantener los datos actualizados, puedes:

1. **Crear un cron job** (Linux/Mac):
```bash
# Ejecutar diariamente a las 8 PM
0 20 * * * cd /ruta/a/tu/proyecto && python app/services/data_ingestion.py
```

2. **Crear una tarea programada** (Windows):
- Abre "Programador de tareas"
- Crea una tarea que ejecute: `python app/services/data_ingestion.py`
- Configura para que se ejecute diariamente

3. **GitHub Actions** (si usas GitHub):
```yaml
# .github/workflows/daily_market_data.yml
name: Daily Market Data Ingestion
on:
  schedule:
    - cron: '0 20 * * *'  # 8 PM UTC diario
  workflow_dispatch:

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python app/services/data_ingestion.py
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_API_KEY: ${{ secrets.SUPABASE_API_KEY }}
```

---

## 🧪 Verificar los Datos

Después de la ingesta, verifica en Supabase:

```sql
-- Ver últimos registros del BCRP
SELECT * FROM bcrp_data ORDER BY fecha DESC LIMIT 10;

-- Ver últimos registros de mercado
SELECT * FROM market_data ORDER BY fecha DESC LIMIT 10;

-- Join para análisis combinado
SELECT 
    b.fecha,
    b.tc_interbancario_venta,
    m.precio_cobre,
    m.indice_dxy
FROM bcrp_data b
LEFT JOIN market_data m ON b.fecha = m.fecha
ORDER BY b.fecha DESC
LIMIT 30;
```

---

## 🎯 Próximos Pasos

Con estos datos ya puedes:

1. ✅ Analizar correlación entre precio del cobre y tipo de cambio
2. ✅ Ver cómo el índice DXY afecta el dólar en Perú
3. ✅ Comparar tasas interbancarias con movimientos del TC
4. 🔜 Agregar datos de noticias para análisis de sentimiento
5. 🔜 Crear modelos predictivos

---

## ❓ Troubleshooting

### Error: "Supabase client no está configurado"
- Verifica que tu `.env` tenga `SUPABASE_URL` y `SUPABASE_API_KEY`

### Error: "relation 'bcrp_data' does not exist"
- Ejecuta primero `python setup_market_tables.py`

### Yahoo Finance no retorna datos
- Verifica tu conexión a internet
- Algunos días (fines de semana) los mercados están cerrados

### BCRP retorna "n.d." (no disponible)
- Es normal para días no laborables o datos aún no publicados
- El script maneja esto automáticamente (inserta NULL)
