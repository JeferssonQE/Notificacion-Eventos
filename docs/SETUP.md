# 🔧 Guía de Configuración

Esta guía te ayudará a configurar el pipeline de datos de DólarBot.

## 📋 Requisitos

- Python 3.11+
- Cuenta de Supabase (gratis)
- Gmail con App Password

---

## 1. Configuración de Gmail

### Paso 1: Habilitar Autenticación de 2 Factores

1. Ve a tu [Cuenta de Google](https://myaccount.google.com/)
2. Navega a `Seguridad`
3. Habilita `Verificación en dos pasos`

### Paso 2: Generar App Password

1. En la misma sección de Seguridad
2. Busca `Contraseñas de aplicaciones`
3. Selecciona `Correo` y `Otro (nombre personalizado)`
4. Escribe "DolarBot" como nombre
5. Copia la contraseña de 16 caracteres generada

### Variables necesarias:
```env
EMAIL_USER=tu_email@gmail.com
EMAIL_PASS=xxxx xxxx xxxx xxxx  # App Password (sin espacios)
EMAIL_TO=destinatario@gmail.com
```

---

## 2. Configuración de Supabase

### Paso 1: Crear Proyecto

1. Ve a [supabase.com](https://supabase.com)
2. Crea una cuenta o inicia sesión
3. Click en `New Project`
4. Completa:
   - **Name**: dolar-bot
   - **Database Password**: (guarda esta contraseña)
   - **Region**: South America (São Paulo)
5. Espera 2-3 minutos mientras se crea el proyecto

### Paso 2: Obtener Credenciales

1. En el dashboard, ve a `Settings` → `API`
2. Copia:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhbGc...`

3. Ve a `Settings` → `Database`
4. Copia la **Connection String** en modo `URI`

### Paso 3: Crear Tabla de Dólar

Ejecuta este SQL en el SQL Editor de Supabase:

```sql
-- Crear tabla dolar
CREATE TABLE dolar (
    id SERIAL PRIMARY KEY,
    origen VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    precio_compra DECIMAL(10, 4) NOT NULL,
    precio_venta DECIMAL(10, 4) NOT NULL,
    diferencia_ayer DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(origen, fecha)
);

-- Crear índices para mejorar performance
CREATE INDEX idx_dolar_origen ON dolar(origen);
CREATE INDEX idx_dolar_fecha ON dolar(fecha DESC);
CREATE INDEX idx_dolar_origen_fecha ON dolar(origen, fecha DESC);
```

### Variables necesarias:
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_API_KEY=eyJhbGc...
SUPABASE_PASSWORD=tu_database_password
SUPABASE_HOST=db.xxxxx.supabase.co
```

---

## 3. Token de SUNAT API

### Opción A: Obtener Token Oficial (Recomendado)

1. Visita la [página de SUNAT](https://e-consulta.sunat.gob.pe/)
2. Inspecciona las peticiones de red (F12 → Network)
3. Busca peticiones a `listarTipoCambio`
4. Copia el token del payload

### Opción B: Token de Prueba

Para desarrollo:
```
TOKEN_SUNAT_API=3eo8o3iyq8e6g8ygwu1kr5azkqpzfa4yk451kyl5aqyhdclc3u9u
```

⚠️ **Nota**: Este token puede expirar. Para producción, obtén tu propio token.

---

## 4. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# SUNAT API
TOKEN_SUNAT_API=tu_token_aqui

# Gmail
EMAIL_USER=tu_email@gmail.com
EMAIL_PASS=tu_app_password_sin_espacios
EMAIL_TO=destinatario@gmail.com

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_API_KEY=eyJhbGc...
SUPABASE_PASSWORD=tu_database_password
SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
```

---

## 5. GitHub Actions Secrets

Para automatización:

### Paso 1: Ir a Settings

1. En tu repositorio de GitHub
2. Ve a `Settings` → `Secrets and variables` → `Actions`
3. Click en `New repository secret`

### Paso 2: Agregar Secrets

| Nombre | Valor | Descripción |
|--------|-------|-------------|
| `TOKEN_SUNAT_API` | `3eo8o3i...` | Token de la API de SUNAT |
| `EMAIL_USER` | `tu@gmail.com` | Tu email de Gmail |
| `EMAIL_PASS` | `xxxxxxxxxxxx` | App Password (sin espacios) |
| `EMAIL_TO` | `destino@email.com` | Email que recibirá el reporte |
| `SUPABASE_URL` | `https://xxx.supabase.co` | URL de tu proyecto |
| `SUPABASE_API_KEY` | `eyJhbGc...` | API Key anon/public |

---

## ✅ Verificación

### Checklist

- [ ] Gmail App Password generado
- [ ] Proyecto Supabase creado
- [ ] Tabla `dolar` creada en Supabase
- [ ] Archivo `.env` configurado
- [ ] Secrets configurados en GitHub

### Prueba Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar ETL
python -m app.services.infrastructure.test_gmail

# Iniciar dashboard
streamlit run app/dashboard/main.py
```

---

## 🆘 Problemas Comunes

### "Authentication failed" en Gmail
- Verifica que uses App Password, no tu contraseña normal
- Asegúrate de que 2FA esté habilitado
- Elimina espacios del App Password

### "Invalid token" en SUNAT
- El token puede haber expirado
- Obtén un nuevo token

### "Connection refused" en Supabase
- Verifica que el proyecto esté activo
- Revisa que la URL y API Key sean correctas

---

**Última actualización**: Diciembre 2024
