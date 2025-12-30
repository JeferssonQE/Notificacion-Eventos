"""
Script de configuración para las nuevas funcionalidades de analytics
"""
import sys
from pathlib import Path

print("="*70)
print("🚀 CONFIGURACIÓN DE ANALYTICS - Sistema de Monitoreo del Dólar")
print("="*70)

print("\n📋 CHECKLIST DE CONFIGURACIÓN:\n")

# 1. Verificar estructura de archivos
print("1️⃣ Verificando archivos creados...")
required_files = [
    ".github/workflows/hourly_scraping.yml",
    "app/scraper/hourly_scraper.py",
    "app/analytics/price_analysis.py",
    "app/analytics/daily_report.py",
    "app/db/migrations/create_dolar_hourly_table.sql",
]

all_exist = True
for file in required_files:
    if Path(file).exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - FALTA")
        all_exist = False

if all_exist:
    print("\n   ✅ Todos los archivos necesarios están presentes")
else:
    print("\n   ⚠️ Algunos archivos faltan, revisa la instalación")

# 2. Verificar dependencias
print("\n2️⃣ Verificando dependencias de Python...")
try:
    import requests
    import beautifulsoup4
    import supabase
    import selenium
    print("   ✅ Dependencias principales instaladas")
except ImportError as e:
    print(f"   ❌ Falta dependencia: {e}")
    print("   Ejecuta: pip install -r requirements.txt")

# 3. Verificar variables de entorno
print("\n3️⃣ Verificando variables de entorno...")
import os
from dotenv import load_dotenv

load_dotenv()

env_vars = {
    "SUPABASE_URL": os.getenv("SUPABASE_URL"),
    "SUPABASE_API_KEY": os.getenv("SUPABASE_API_KEY"),
    "TOKEN_SUNAT_API": os.getenv("TOKEN_SUNAT_API"),
    "EMAIL_USER": os.getenv("EMAIL_USER"),
    "EMAIL_PASS": os.getenv("EMAIL_PASS"),
    "EMAIL_TO": os.getenv("EMAIL_TO"),
}

all_env_set = True
for var, value in env_vars.items():
    if value:
        print(f"   ✅ {var}")
    else:
        print(f"   ❌ {var} - NO CONFIGURADA")
        all_env_set = False

if not all_env_set:
    print("\n   ⚠️ Configura las variables faltantes en .env")

# 4. Instrucciones para Supabase
print("\n4️⃣ Configuración de Base de Datos (Supabase):")
print("   📝 Pasos:")
print("   1. Abre Supabase Dashboard")
print("   2. Ve a SQL Editor")
print("   3. Copia el contenido de: app/db/migrations/create_dolar_hourly_table.sql")
print("   4. Ejecuta el script SQL")
print("   5. Verifica que la tabla 'dolar_hourly' se creó correctamente")

# 5. Instrucciones para GitHub Actions
print("\n5️⃣ Configuración de GitHub Actions:")
print("   📝 Pasos:")
print("   1. Ve a tu repositorio en GitHub")
print("   2. Settings → Secrets and variables → Actions")
print("   3. Verifica que todos los secrets estén configurados:")
for var in env_vars.keys():
    print(f"      - {var}")
print("   4. Ve a Actions → Workflows")
print("   5. Habilita 'Scraping-Horario-Casas-Cambio'")
print("   6. Ejecuta manualmente para probar (Run workflow)")

# 6. Prueba rápida
print("\n6️⃣ Prueba Rápida:")
print("   Ejecuta: python test_analytics.py")
print("   Esto verificará que todo funcione correctamente")

# 7. Próximos pasos
print("\n" + "="*70)
print("✅ CONFIGURACIÓN COMPLETADA")
print("="*70)

print("\n📚 DOCUMENTACIÓN:")
print("   • ANALYTICS_FEATURES.md - Documentación técnica completa")
print("   • MEJORAS_IMPLEMENTADAS.md - Resumen ejecutivo y valor agregado")

print("\n🎯 PRÓXIMOS PASOS:")
print("   1. Ejecuta el SQL en Supabase (paso 4)")
print("   2. Configura GitHub Secrets (paso 5)")
print("   3. Ejecuta: python test_analytics.py")
print("   4. Activa el workflow horario")
print("   5. Espera 2-3 horas para acumular datos")
print("   6. Ejecuta: python -m app.analytics.price_analysis")
print("   7. Revisa tu email con los nuevos insights")

print("\n💡 TIPS:")
print("   • El scraping horario se ejecuta cada 2h de 8am a 8pm")
print("   • Necesitas al menos 2-3 capturas para ver análisis significativos")
print("   • El reporte diario se envía a la 1:00 PM (hora Lima)")
print("   • Puedes ejecutar manualmente cualquier script con 'python -m'")

print("\n📞 SOPORTE:")
print("   Si tienes problemas, revisa:")
print("   • Los logs de GitHub Actions")
print("   • La consola de Supabase")
print("   • Los archivos de documentación")

print("\n" + "="*70)
print("🎉 ¡Listo para usar el sistema de analytics!")
print("="*70 + "\n")
