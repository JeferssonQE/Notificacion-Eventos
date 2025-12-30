# 📊 Análisis Estratégico de Casas de Cambio

## Nuevas Funcionalidades

### 1. **Scraping Horario** 🕐
Captura datos cada 2 horas (8am - 8pm) para análisis de variaciones intradiarias.

**Archivo**: `.github/workflows/hourly_scraping.yml`
**Script**: `app/scraper/hourly_scraper.py`

**Datos capturados**:
- Precio de compra y venta
- Timestamp exacto
- Spread (diferencia venta-compra)
- URL de la casa de cambio

### 2. **Análisis de Variaciones** 📈
Calcula métricas estratégicas para cada casa de cambio.

**Archivo**: `app/analytics/price_analysis.py`

**Métricas calculadas**:
- ✅ Variación 1 hora
- ✅ Variación 24 horas
- ✅ Variación 7 días
- ✅ Volatilidad (desviación estándar)
- ✅ Spread promedio/mínimo/máximo
- ✅ Ranking de estabilidad
- ✅ Detección de arbitraje

### 3. **Reporte Diario Mejorado** 📧
Email con insights estratégicos automáticos.

**Archivo**: `app/analytics/daily_report.py`

**Incluye**:
- 🏆 Top 3 casas más estables (menor volatilidad)
- 💎 Top 3 mejor spread promedio
- 📈 Top 3 mayores variaciones 24h
- 💰 Mejores oportunidades actuales
- 🚀 Alertas de arbitraje

## Estructura de Base de Datos

### Nueva tabla: `dolar_hourly`

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

**Índices optimizados** para consultas rápidas:
- Por origen
- Por fecha
- Por timestamp
- Compuesto (origen + timestamp)

## Uso

### Ejecutar scraping horario manualmente
```bash
python -m app.scraper.hourly_scraper
```

### Generar análisis de casas
```bash
python -m app.analytics.price_analysis
```

### Generar reporte diario
```bash
python -m app.analytics.daily_report
```

### Enviar email con insights
```bash
python -m app.services.infrastructure.test_gmail
```

## Configuración en Supabase

1. Ejecuta el script SQL:
```bash
psql -h <tu-host> -U <tu-usuario> -d <tu-db> -f app/db/migrations/create_dolar_hourly_table.sql
```

O copia el contenido del archivo y ejecútalo en el SQL Editor de Supabase.

## GitHub Actions

### Workflows configurados:

1. **`daily.yml`** - Reporte diario (1:00 PM Lima)
2. **`hourly_scraping.yml`** - Scraping cada 2 horas (8am-8pm Lima)

### Secrets requeridos:
- `SUPABASE_URL`
- `SUPABASE_API_KEY`
- `TOKEN_SUNAT_API`
- `EMAIL_USER`
- `EMAIL_PASS`
- `EMAIL_TO`

## Beneficios para tu CV

### Antes:
> "Construí un pipeline ETL que extrae el tipo de cambio del dólar"

### Ahora:
> "Desarrollé sistema de análisis estratégico con scraping horario (cada 2h) que calcula volatilidad, spread y detecta oportunidades de arbitraje en tiempo real. Implementé métricas avanzadas (desviación estándar, variaciones multi-período) y reportes automatizados con insights accionables."

## Próximas Mejoras Sugeridas

- [ ] Dashboard interactivo con Streamlit
- [ ] API REST para consultas externas
- [ ] Predicción de tendencias con ML (Prophet/ARIMA)
- [ ] Alertas por Telegram/Discord
- [ ] Tests unitarios con pytest
- [ ] Monitoreo con Prometheus
- [ ] Compresión de datos históricos

## Ejemplos de Insights Generados

### Casas más estables (confiables):
1. Rextie - Volatilidad: 0.0012
2. Kambista - Volatilidad: 0.0015
3. Cambios Liberty - Volatilidad: 0.0018

### Mejor spread promedio:
1. Rextie - Spread: 0.0050
2. Kambista - Spread: 0.0065
3. Cambios Online - Spread: 0.0080

### Mayores variaciones 24h:
1. Casa X - ▲ 0.0250 (subió)
2. Casa Y - ▼ 0.0180 (bajó)
3. Casa Z - ▲ 0.0120 (subió)

## Contacto

Desarrollado por Jefersson Kevin Quicaña Erquinio
- GitHub: github.com/JeferssonQE
- Email: jefersson.quicana@utec.edu.pe
