"""
Script para probar la API localmente
Ejecuta: python test_api_local.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_api():
    print("\n🚀 Iniciando pruebas de API...")
    
    # 1. Health check
    try:
        r = requests.get(f"{BASE_URL}/api/health")
        print_response("Health Check", r)
    except Exception as e:
        print(f"❌ Error en health check: {e}")
    
    # 2. Root endpoint
    try:
        r = requests.get(f"{BASE_URL}/")
        print_response("Root Endpoint", r)
    except Exception as e:
        print(f"❌ Error en root: {e}")
    
    # 3. Últimos precios de casas
    try:
        r = requests.get(f"{BASE_URL}/api/v1/casas/latest")
        print_response("Últimos Precios Casas", r)
    except Exception as e:
        print(f"❌ Error en casas/latest: {e}")
    
    # 4. Analytics de casas
    try:
        r = requests.get(f"{BASE_URL}/api/v1/casas/analytics?days=7")
        print_response("Analytics Casas (7 días)", r)
    except Exception as e:
        print(f"❌ Error en casas/analytics: {e}")
    
    # 5. Oportunidades
    try:
        r = requests.get(f"{BASE_URL}/api/v1/casas/opportunities")
        print_response("Oportunidades de Trading", r)
    except Exception as e:
        print(f"❌ Error en opportunities: {e}")
    
    # 6. BCRP latest
    try:
        r = requests.get(f"{BASE_URL}/api/v1/bcrp/latest")
        print_response("BCRP Último Dato", r)
    except Exception as e:
        print(f"❌ Error en bcrp/latest: {e}")
    
    # 7. Market latest
    try:
        r = requests.get(f"{BASE_URL}/api/v1/market/latest")
        print_response("Market Último Dato", r)
    except Exception as e:
        print(f"❌ Error en market/latest: {e}")
    
    # 8. Dashboard summary
    try:
        r = requests.get(f"{BASE_URL}/api/v1/dashboard/summary")
        print_response("Dashboard Summary", r)
    except Exception as e:
        print(f"❌ Error en dashboard/summary: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Pruebas completadas")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    print("\n⚠️  Asegúrate de que la API esté corriendo:")
    print("   uvicorn app.main:app --reload\n")
    
    input("Presiona ENTER para continuar...")
    test_api()
