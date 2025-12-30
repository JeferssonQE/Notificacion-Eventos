"""
Script de prueba para verificar las nuevas funcionalidades de analytics
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("="*60)
print("🧪 PRUEBA DE FUNCIONALIDADES DE ANALYTICS")
print("="*60)

# Test 1: Scraping horario
print("\n1️⃣ Probando scraping horario...")
try:
    from app.scraper.hourly_scraper import scrape_and_store_hourly
    result = scrape_and_store_hourly()
    if result:
        print("✅ Scraping horario funcionando correctamente")
    else:
        print("⚠️ Scraping completado con advertencias")
except Exception as e:
    print(f"❌ Error en scraping horario: {e}")

# Test 2: Análisis de precios
print("\n2️⃣ Probando análisis de variaciones...")
try:
    from app.analytics.price_analysis import get_best_opportunities
    opportunities = get_best_opportunities()
    if opportunities:
        print("✅ Análisis de oportunidades funcionando")
        if opportunities.get("best_buy"):
            print(f"   Mejor compra: {opportunities['best_buy']['casa']}")
        if opportunities.get("arbitrage", {}).get("possible"):
            print("   🚀 ¡Arbitraje detectado!")
    else:
        print("⚠️ No hay datos suficientes para análisis")
except Exception as e:
    print(f"❌ Error en análisis: {e}")

# Test 3: Reporte diario
print("\n3️⃣ Probando generación de reporte...")
try:
    from app.analytics.daily_report import generate_daily_insights, format_insights_for_email
    insights = generate_daily_insights()
    html = format_insights_for_email(insights)
    
    if insights and html:
        print("✅ Reporte diario generado correctamente")
        print(f"   Casas analizadas: {insights.get('total_casas_analyzed', 0)}")
        print(f"   HTML generado: {len(html)} caracteres")
    else:
        print("⚠️ Reporte generado pero sin datos")
except Exception as e:
    print(f"❌ Error en reporte: {e}")

# Test 4: Email con insights
print("\n4️⃣ Probando integración con email...")
try:
    from app.services.infrastructure.test_gmail import send_gmail_with_dolar
    print("⚠️ No se enviará email real (comentar para probar)")
    # send_gmail_with_dolar()  # Descomentar para enviar email real
    print("✅ Módulo de email cargado correctamente")
except Exception as e:
    print(f"❌ Error en módulo de email: {e}")

print("\n" + "="*60)
print("✅ PRUEBAS COMPLETADAS")
print("="*60)
print("\n📝 Próximos pasos:")
print("1. Ejecuta el SQL en Supabase: app/db/migrations/create_dolar_hourly_table.sql")
print("2. Activa el workflow horario en GitHub Actions")
print("3. Espera algunas horas para acumular datos")
print("4. Ejecuta: python -m app.analytics.price_analysis")
print("5. Revisa el email diario con los nuevos insights")
