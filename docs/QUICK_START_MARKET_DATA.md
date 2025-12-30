# 🚀 Quick Start - Market Data

## Paso 1: Instalar yfinance
```bash
pip install yfinance
```

## Paso 2: Probar que los servicios funcionan
```bash
python test_market_services.py
```

Deberías ver datos del BCRP y Yahoo Finance. Si ves errores, revisa tu conexión a internet.

## Paso 3: Crear las tablas en Supabase
```bash
python setup_market_tables.py
```

Si falla, copia el SQL de `app/db/migrations/create_market_data_tables.sql` y ejecútalo manualmente en Supabase.

## Paso 4: Ingestar datos (últimos 30 días)
```bash
python app/services/data_ingestion.py
```

## Paso 5: Verificar en Supabase

Ve a tu proyecto Supabase → SQL Editor y ejecuta:

```sql
SELECT COUNT(*) FROM bcrp_data;
SELECT COUNT(*) FROM market_data;

-- Ver últimos datos
SELECT * FROM bcrp_data ORDER BY fecha DESC LIMIT 5;
SELECT * FROM market_data ORDER BY fecha DESC LIMIT 5;
```

## ✅ Listo!

Ahora tienes:
- ✅ Datos del BCRP (tipo de cambio interbancario + tasa)
- ✅ Datos de mercado (precio cobre + índice dólar)
- ✅ Todo guardado en tu BD para análisis

## 🎯 Siguiente: Agregar Noticias

Cuando estés listo, podemos agregar el módulo de noticias para análisis de sentimiento.
