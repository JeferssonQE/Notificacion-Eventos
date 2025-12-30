# 🧪 Scripts de Prueba y Setup

Esta carpeta contiene scripts para probar funcionalidades y configurar el proyecto.

## 🔧 Scripts de Setup

### setup_analytics.py
Configura las tablas de analytics en Supabase.
```bash
python tests_scripts/setup_analytics.py
```

### setup_market_tables.py
Crea las tablas de datos de mercado (BCRP, Market).
```bash
python tests_scripts/setup_market_tables.py
```

## 🧪 Scripts de Prueba

### test_api_local.py
Prueba todos los endpoints de la API REST.
```bash
# Asegúrate de que la API esté corriendo
uvicorn app.main:app --reload

# En otra terminal
python tests_scripts/test_api_local.py
```

### test_celery_tasks.py
Prueba las tareas de Celery.
```bash
# Asegúrate de que Redis y Celery estén corriendo
docker run -d -p 6379:6379 redis:alpine
celery -A app.celery.config worker --loglevel=info --pool=solo

# En otra terminal
python tests_scripts/test_celery_tasks.py
```

### test_analytics.py
Prueba las funcionalidades de analytics.
```bash
python tests_scripts/test_analytics.py
```

### test_market_services.py
Prueba los servicios de datos de mercado (BCRP, Yahoo Finance).
```bash
python tests_scripts/test_market_services.py
```

## 📝 Notas

- Todos los scripts requieren que el archivo `.env` esté configurado correctamente
- Los scripts de setup solo necesitan ejecutarse una vez
- Los scripts de prueba pueden ejecutarse múltiples veces

---

**Volver a**: [README principal](../README.md) | [Documentación técnica](../DOCS.md)
