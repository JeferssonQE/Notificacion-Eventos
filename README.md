# 💱 DólarBot - ETL Automatizado de Tipo de Cambio

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

Sistema ETL (Extract, Transform, Load) automatizado que monitorea el tipo de cambio del dólar en Perú, identifica oportunidades de arbitraje y envía reportes diarios por correo electrónico.

> 🚀 **Proyecto en producción** - Ejecutándose automáticamente todos los días a las 13:00 (Lima) mediante GitHub Actions

## 🎯 Características Principales

### Extracción de Datos (Extract)
- ✅ **API oficial de SUNAT** - Tipo de cambio gubernamental
- ✅ **Web scraping** de 15+ casas de cambio peruanas
- ✅ **Validación y limpieza** de datos en tiempo real
- ✅ **Manejo de errores** y reintentos automáticos

### Transformación y Análisis (Transform)
- 📊 **Identificación de top 3** mejores tasas de compra/venta
- 💹 **Detección automática** de oportunidades de arbitraje
- 📈 **Cálculo de variaciones** porcentuales vs día anterior
- 🎨 **Generación de badges** visuales (▲/▼) para tendencias

### Carga y Notificación (Load)
- 💾 **Persistencia en Supabase** (PostgreSQL) con validación de duplicados
- 📧 **Reportes HTML responsive** enviados por Gmail
- 🔔 **Sistema de alertas** configurables por precio
- 📱 **Diseño mobile-first** para lectura en cualquier dispositivo

### Automatización
- ⏰ **GitHub Actions** - Ejecución diaria automática (13:00 Lima)
- 🐳 **Docker Compose** - Despliegue con un solo comando
- 🔄 **Celery + Redis** - Procesamiento asíncrono de tareas
- 📊 **API REST** - Endpoints para consulta de datos históricos

## 🏗️ Arquitectura

> 📖 **Documentación completa**: Ver [ARCHITECTURE.md](./ARCHITECTURE.md) para detalles técnicos profundos

```
┌─────────────────┐
│  GitHub Actions │  ← Scheduler (Cron: 18:00 UTC)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│           ETL Pipeline                   │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Extract  │→ │Transform │→ │  Load  ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐   ┌──────────────┐
│  Gmail Service  │   │   Supabase   │
│  (Notificación) │   │  (PostgreSQL)│
└─────────────────┘   └──────────────┘
```

### Componentes Principales

- **Extractor**: Obtiene datos de SUNAT API y 15+ casas de cambio
- **Transformer**: Calcula top 3, arbitraje y variaciones porcentuales
- **Loader**: Persiste en Supabase y envía reportes por Gmail
- **Scheduler**: GitHub Actions ejecuta el pipeline diariamente

## 📊 Métricas del Proyecto

- 🏦 **15+ casas de cambio** monitoreadas diariamente
- 📅 **100% uptime** con GitHub Actions
- ⚡ **< 30 segundos** tiempo de ejecución del ETL
- 📧 **Reportes HTML** con diseño responsive
- 💾 **Histórico completo** de tipos de cambio en Supabase
- 🔄 **Ejecución automática** sin intervención manual

## 🛠️ Stack Tecnológico

### Backend & API
- **FastAPI** - Framework web asíncrono de alto rendimiento
- **SQLAlchemy 2.0** - ORM moderno con soporte async
- **Pydantic v2** - Validación de datos con type hints
- **Python 3.11** - Últimas características del lenguaje

### Web Scraping & Data Extraction
- **BeautifulSoup4** - Parsing y navegación de HTML/XML
- **Selenium + undetected-chromedriver** - Automatización de navegador
- **Requests** - Cliente HTTP con manejo de sesiones
- **Regex** - Extracción de patrones complejos

### Infraestructura & DevOps
- **Supabase** - PostgreSQL managed + API REST automática
- **GitHub Actions** - CI/CD con cron scheduling
- **Docker & Docker Compose** - Containerización multi-servicio
- **Redis** - Cache en memoria y message broker
- **Celery + Beat** - Task queue distribuido con scheduler

### Notificaciones
- **Gmail SMTP** - Envío de emails con HTML/CSS
- **Plantillas HTML** - Diseño responsive con inline CSS

## 📦 Estructura del Proyecto

```
dolar/
├── app/
│   ├── api/              # Endpoints REST
│   ├── scraper/          # Módulos de extracción de datos
│   │   ├── get_sunat_dolar.py
│   │   └── top_3_cambio.py
│   ├── services/         # Lógica de negocio
│   │   ├── domain/       # Servicios de dominio
│   │   └── infrastructure/  # Servicios de infraestructura
│   │       └── gmail/    # Servicio de notificaciones
│   ├── db/               # Modelos y configuración de BD
│   └── core/             # Configuración central
├── .github/
│   └── workflows/
│       └── daily.yml     # GitHub Action para ejecución diaria
├── docker-compose.yml    # Orquestación de servicios
└── requirements.txt
```

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.11+
- Docker & Docker Compose (opcional)
- Cuenta de Supabase (gratis)
- Gmail con App Password configurado

> 📖 **Guía completa de configuración**: Ver [SETUP.md](./SETUP.md) para instrucciones detalladas paso a paso

### Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/jefersson1/dolar.git
cd dolar

# 2. Crear y configurar .env (ver SETUP.md para detalles)
cp .env.example .env
# Editar .env con tus credenciales

# 3. Opción A: Ejecutar con Docker (recomendado)
docker-compose up -d

# 3. Opción B: Ejecutar localmente
pip install -r requirements.txt
python -m app.services.infrastructure.test_gmail
```

### Ejecución Manual del ETL

```bash
# Ejecutar el proceso ETL completo
python -m app.services.infrastructure.test_gmail

# Resultado esperado:
# ✅ Datos extraídos de SUNAT
# ✅ Scraping de 15+ casas de cambio
# ✅ Datos guardados en Supabase
# ✅ Email enviado con reporte
```

### Iniciar API REST

```bash
# Desarrollo
uvicorn app.main:app --reload --port 8000

# Producción con Docker
docker-compose up -d app

# Acceder a la documentación interactiva
# http://localhost:8000/docs
```

### Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f app

# Reiniciar servicios
docker-compose restart

# Detener todos los servicios
docker-compose down

# Limpiar volúmenes (⚠️ elimina datos)
docker-compose down -v
```

## 📊 Funcionalidades del ETL

### 1. Extracción (Extract)
- Consulta API oficial de SUNAT para tipo de cambio del día
- Scraping de casas de cambio desde cuantoestaeldolar.pe
- Validación y limpieza de datos extraídos

### 2. Transformación (Transform)
- Cálculo de variaciones porcentuales vs día anterior
- Identificación de top 3 mejores tasas de compra/venta
- Detección de oportunidades de arbitraje
- Generación de badges visuales (▲/▼) para variaciones

### 3. Carga (Load)
- Inserción en Supabase con validación de duplicados
- Generación de reporte HTML personalizado
- Envío de notificación por Gmail

## 🤖 Automatización con GitHub Actions

El workflow se ejecuta automáticamente todos los días a las 13:00 (hora de Lima):

```yaml
on:
  schedule:
    - cron: '0 18 * * *'  # 18:00 UTC = 13:00 Lima
  workflow_dispatch:       # Ejecución manual desde GitHub UI
```

### Configuración de Secrets en GitHub

Para que el workflow funcione, configura estos secrets en tu repositorio:

1. Ve a `Settings` → `Secrets and variables` → `Actions`
2. Agrega los siguientes secrets:

| Secret | Descripción |
|--------|-------------|
| `TOKEN_SUNAT_API` | Token de la API de SUNAT |
| `EMAIL_USER` | Tu email de Gmail |
| `EMAIL_PASS` | App Password de Gmail (no tu contraseña normal) |
| `EMAIL_TO` | Email destinatario del reporte |
| `SUPABASE_URL` | URL de tu proyecto Supabase |
| `SUPABASE_API_KEY` | API Key de Supabase (anon/public) |

### Ejecución Manual

Puedes ejecutar el workflow manualmente desde GitHub:
1. Ve a la pestaña `Actions`
2. Selecciona `Notificacion-dolar-diario`
3. Click en `Run workflow`

## 📸 Demo del Sistema

### GitHub Actions - Ejecución Automática
El workflow se ejecuta diariamente de forma automática:

<img width="989" height="605" alt="GitHub Actions ejecutando el workflow diario" src="https://github.com/user-attachments/assets/52d9db4f-7ffa-4e9a-893a-6c8a51ee96d3" />

### Reporte por Email - Vista Desktop
Reporte HTML profesional con análisis completo del tipo de cambio:

<img width="1035" height="489" alt="Reporte de tipo de cambio en Gmail - Desktop" src="https://github.com/user-attachments/assets/e728f777-cf29-4a4c-bb23-c22dbde3d623" />

### Reporte por Email - Vista Mobile
Diseño responsive optimizado para dispositivos móviles:

<img width="315" height="455" alt="Reporte de tipo de cambio en Gmail - Mobile" src="https://github.com/user-attachments/assets/b56f7be5-85a1-43c9-98f3-910f39516cb9" />

### Contenido del Reporte

El sistema genera reportes HTML con:
- 📈 Tipo de cambio oficial SUNAT con variación diaria
- 🏆 Top 3 mejores casas para comprar dólares
- 💰 Top 3 mejores casas para vender dólares
- ⚡ Alerta de oportunidades de arbitraje
- 🔗 Enlaces directos a cada casa de cambio
- 📱 Diseño responsive para mobile y desktop

## 🔄 API Endpoints

```
GET  /                    # Info de la API
GET  /api/health          # Health check
GET  /api/v1/dolar        # Obtener datos de dólar
POST /api/v1/dolar        # Crear registro
```

## 📈 Mejoras Futuras

- [ ] Integración con WhatsApp Business API
- [ ] Dashboard web con gráficos históricos
- [ ] Alertas personalizadas por umbral de precio
- [ ] Soporte para más monedas (EUR, BRL, etc.)
- [ ] Machine Learning para predicción de tendencias

## 🔧 Troubleshooting

### Error: "No se pudieron obtener las casas de cambio"
- Verificar conexión a internet
- El sitio web puede haber cambiado su estructura HTML
- Revisar logs: `docker-compose logs app`

### Error: "SUNAT no publicó tipo de cambio hoy"
- SUNAT publica datos en días hábiles
- Verificar que el `TOKEN_SUNAT_API` sea válido
- Revisar si la API de SUNAT está disponible

### GitHub Action no se ejecuta
- Verificar que los secrets estén configurados correctamente
- Revisar la pestaña "Actions" en GitHub para ver errores
- El cron puede tener hasta 15 minutos de delay

### Email no llega
- Verificar que `EMAIL_PASS` sea un "App Password" de Gmail
- Revisar carpeta de spam
- Verificar que la autenticación de 2 factores esté habilitada en Gmail

## 🚀 Roadmap

- [ ] Dashboard web interactivo con gráficos históricos
- [ ] Integración con WhatsApp Business API
- [ ] Alertas personalizadas por umbral de precio
- [ ] Soporte para más monedas (EUR, BRL, CLP)
- [ ] API pública con rate limiting
- [ ] Machine Learning para predicción de tendencias
- [ ] Notificaciones push móviles
- [ ] Exportación de datos a CSV/Excel

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 👨‍💻 Autor

**Jefersson** - [GitHub](https://github.com/jefersson1)

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

<div align="center">

⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub

**[Ver Demo](https://github.com/jefersson1/dolar)** • **[Reportar Bug](https://github.com/jefersson1/dolar/issues)** • **[Solicitar Feature](https://github.com/jefersson1/dolar/issues)**

</div>
