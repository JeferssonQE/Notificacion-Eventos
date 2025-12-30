"""
Script para probar tareas de Celery
Ejecuta: python test_celery_tasks.py
"""
from app.celery.task import (
    health_check,
    scrape_hourly_casas,
    ingest_daily_data,
    calculate_analytics,
    detect_arbitrage,
    generate_daily_report
)

def test_celery():
    print("\n🚀 Probando tareas de Celery...")
    print("="*60)
    
    # 1. Health check
    print("\n1️⃣ Health Check")
    try:
        result = health_check.delay()
        print(f"   Task ID: {result.id}")
        print(f"   Status: {result.status}")
        print(f"   Result: {result.get(timeout=10)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Scrape casas
    print("\n2️⃣ Scrape Hourly Casas")
    try:
        result = scrape_hourly_casas.delay()
        print(f"   Task ID: {result.id}")
        print(f"   Status: {result.status}")
        print(f"   Result: {result.get(timeout=30)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Calculate analytics
    print("\n3️⃣ Calculate Analytics")
    try:
        result = calculate_analytics.delay(days=7)
        print(f"   Task ID: {result.id}")
        print(f"   Status: {result.status}")
        print(f"   Result: {result.get(timeout=30)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Detect arbitrage
    print("\n4️⃣ Detect Arbitrage")
    try:
        result = detect_arbitrage.delay()
        print(f"   Task ID: {result.id}")
        print(f"   Status: {result.status}")
        print(f"   Result: {result.get(timeout=30)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ Pruebas completadas")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("\n⚠️  Asegúrate de que Redis y Celery worker estén corriendo:")
    print("   Terminal 1: redis-server")
    print("   Terminal 2: celery -A app.celery.config worker --loglevel=info --pool=solo\n")
    
    input("Presiona ENTER para continuar...")
    test_celery()
