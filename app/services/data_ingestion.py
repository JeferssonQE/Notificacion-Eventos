"""
Data Ingestion Service
Ingesta datos de BCRP, mercado internacional y casas de cambio a Supabase.
"""
from datetime import datetime, timedelta
from typing import Dict, List

from app.services.bcrp_service import get_bcrp_data
from app.services.market_service import get_international_data
from app.scraper.casas_scraper import scrape_casas_cambio
from app.db.supabase.client import get_supabase_client


def insert_casas_data(casas: List[Dict], fecha: str) -> Dict[str, int]:
    """
    Inserta datos de casas de cambio en Supabase.
    
    Args:
        casas: Lista de casas scrapeadas
        fecha: Fecha en formato 'YYYY-MM-DD'
        
    Returns:
        Dict con contadores de insertados y errores
    """
    if not casas:
        print("⚠️  No hay datos de casas para insertar")
        return {"inserted": 0, "errors": 0}
    
    supabase = get_supabase_client()
    inserted = 0
    errors = 0
    
    for casa in casas:
        try:
            # Verificar si ya existe
            existing = supabase.table("dolar")\
                .select("*")\
                .eq("origen", casa["nombre"])\
                .eq("fecha", fecha)\
                .execute()
            
            if existing.data:
                print(f"⚠️  {casa['nombre']} ya existe para {fecha}")
                continue
            
            # Insertar
            casa_data = {
                "origen": casa["nombre"],
                "fecha": fecha,
                "precio_compra": casa["compra"],
                "precio_venta": casa["venta"],
            }
            
            supabase.table("dolar").insert(casa_data).execute()
            inserted += 1
            print(f"✅ Casa: {casa['nombre']} - Compra: {casa['compra']}, Venta: {casa['venta']}")
            
        except Exception as e:
            errors += 1
            print(f"❌ Error insertando {casa.get('nombre')}: {e}")
    
    return {"inserted": inserted, "errors": errors}


def insert_bcrp_data(records: List[Dict]) -> Dict[str, int]:
    """
    Inserta o actualiza datos del BCRP en Supabase.
    
    Args:
        records: Lista de diccionarios con datos del BCRP
        
    Returns:
        Dict con contadores de insertados y errores
    """
    if not records:
        print("⚠️  No hay datos del BCRP para insertar")
        return {"inserted": 0, "errors": 0}
    
    supabase = get_supabase_client()
    inserted = 0
    errors = 0
    
    for record in records:
        try:
            supabase.table("bcrp_data").upsert(
                record,
                on_conflict="fecha"
            ).execute()
            
            inserted += 1
            tc = record.get('tc_interbancario_venta', 'N/A')
            print(f"✅ BCRP: {record['fecha']} - TC: {tc}")
            
        except Exception as e:
            errors += 1
            print(f"❌ Error BCRP {record.get('fecha')}: {e}")
    
    return {"inserted": inserted, "errors": errors}

def insert_market_data(records: List[Dict]) -> Dict[str, int]:
    """
    Inserta o actualiza datos de mercado internacional en Supabase.
    
    Args:
        records: Lista de diccionarios con datos de Yahoo Finance
        
    Returns:
        Dict con contadores de insertados y errores
    """
    if not records:
        print("⚠️  No hay datos de mercado para insertar")
        return {"inserted": 0, "errors": 0}
    
    supabase = get_supabase_client()
    inserted = 0
    errors = 0
    
    for record in records:
        try:
            supabase.table("market_data").upsert(
                record,
                on_conflict="fecha"
            ).execute()
            
            inserted += 1
            cobre = record.get('precio_cobre', 'N/A')
            dxy = record.get('indice_dxy', 'N/A')
            print(f"✅ Market: {record['fecha']} - Cobre: {cobre}, DXY: {dxy}")
            
        except Exception as e:
            errors += 1
            print(f"❌ Error Market {record.get('fecha')}: {e}")
    
    return {"inserted": inserted, "errors": errors}

def ingest_data(start_date: str, end_date: str) -> None:
    """
    Orquesta la ingesta completa de datos.
    
    Args:
        start_date: Fecha inicio en formato 'YYYY-MM-DD'
        end_date: Fecha fin en formato 'YYYY-MM-DD'
    """
    print(f"\n{'='*60}")
    print(f"🚀 Ingesta de datos: {start_date} → {end_date}")
    print(f"{'='*60}\n")
    
    # Extraer datos
    print("📊 Extrayendo datos del BCRP...")
    bcrp_records = get_bcrp_data(start_date, end_date)
    print(f"   Obtenidos: {len(bcrp_records)} registros\n")
    
    print("🌎 Extrayendo datos de Yahoo Finance...")
    market_records = get_international_data(start_date, end_date)
    print(f"   Obtenidos: {len(market_records)} registros\n")
    
    print("🏦 Extrayendo datos de casas de cambio...")
    casas = scrape_casas_cambio()
    print(f"   Obtenidas: {len(casas)} casas\n")
    
    # Insertar datos
    print("💾 Insertando datos del BCRP...")
    bcrp_result = insert_bcrp_data(bcrp_records)
    print(f"   ✅ Insertados: {bcrp_result['inserted']}")
    print(f"   ❌ Errores: {bcrp_result['errors']}\n")
    
    print("💾 Insertando datos de mercado...")
    market_result = insert_market_data(market_records)
    print(f"   ✅ Insertados: {market_result['inserted']}")
    print(f"   ❌ Errores: {market_result['errors']}\n")
    
    print("💾 Insertando datos de casas...")
    casas_result = insert_casas_data(casas, end_date)
    print(f"   ✅ Insertados: {casas_result['inserted']}")
    print(f"   ❌ Errores: {casas_result['errors']}\n")
    
    # Resumen
    total = bcrp_result['inserted'] + market_result['inserted'] + casas_result['inserted']
    print(f"{'='*60}")
    print(f"✨ Ingesta completada: {total} registros totales")
    print(f"{'='*60}\n")

def ingest_today() -> None:
    """Ingesta datos del día actual."""
    today = datetime.now().strftime("%Y-%m-%d")
    ingest_data(today, today)

def ingest_historical(start_year: int = 2020) -> None:
    """
    Ingesta datos históricos desde un año específico.
    
    Args:
        start_year: Año de inicio (ej: 2020)
    """
    start_date = f"{start_year}-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")
    ingest_data(start_date, end_date)

if __name__ == "__main__":
    # Ingesta hoy
    ingest_today()
    
    # Otras opciones:
    # ingest_today()                              # Solo hoy
    # ingest_historical(2020)                     # Desde 2020
    # ingest_data("2024-01-01", "2024-12-31")     # Rango específico
