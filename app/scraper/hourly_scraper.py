"""
Scraper horario para capturar variaciones de precios durante el día
"""
from datetime import datetime

from app.scraper.casas_scraper import scrape_casas_cambio
from app.db.supabase.config import supabase


def insert_hourly_data(data):
    """Inserta datos con timestamp exacto (hora incluida)"""
    try:
        result = supabase.table("dolar_hourly").insert(data).execute()
        print(f"✅ Insertado: {data['origen']} - {data['timestamp']}")
        return result
    except Exception as e:
        print(f"❌ Error insertando {data['origen']}: {e}")
        return None


def scrape_and_store_hourly():
    """Captura datos de todas las casas y los guarda con timestamp"""
    print(f"\n{'='*60}")
    print(f"🕐 Iniciando scraping horario: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        casas = scrape_casas_cambio()
        timestamp = datetime.now().isoformat()
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")
        
        inserted_count = 0
        for casa in casas:
            data = {
                "origen": casa["nombre"],
                "fecha": fecha,
                "hora": hora,
                "timestamp": timestamp,
                "precio_compra": casa["compra"],
                "precio_venta": casa["venta"],
                "spread": round(casa["venta"] - casa["compra"], 4),
                "url": casa.get("url", ""),
            }
            
            result = insert_hourly_data(data)
            if result:
                inserted_count += 1
        
        print(f"\n✅ Scraping completado: {inserted_count}/{len(casas)} casas guardadas")
        return True
        
    except Exception as e:
        print(f"❌ Error en scraping horario: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    scrape_and_store_hourly()
