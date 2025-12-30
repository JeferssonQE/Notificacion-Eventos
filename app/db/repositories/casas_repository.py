"""
Repository para operaciones de base de datos de casas de cambio
"""
from datetime import datetime
from typing import Dict, List, Optional

from app.db.supabase.client import get_supabase_client


def insert_casa_precio(casa_data: Dict) -> bool:
    """
    Inserta precio de una casa de cambio en la base de datos.
    Evita duplicados verificando fecha y origen.
    
    Args:
        casa_data: Dict con datos de la casa
        {
            "origen": "Rextie",
            "fecha": "2025-12-30",
            "precio_compra": 3.75,
            "precio_venta": 3.78
        }
        
    Returns:
        True si se insertó correctamente
    """
    try:
        supabase = get_supabase_client()
        
        # Verificar si ya existe
        existing = supabase.table("dolar")\
            .select("*")\
            .eq("origen", casa_data.get("origen"))\
            .eq("fecha", casa_data.get("fecha"))\
            .execute()
        
        if existing.data:
            print(f"⚠️  {casa_data.get('origen')} ya existe para {casa_data.get('fecha')}")
            return False
        
        # Insertar
        supabase.table("dolar").insert(casa_data).execute()
        print(f"✅ Insertado: {casa_data.get('origen')} - {casa_data.get('fecha')}")
        return True
        
    except Exception as e:
        print(f"❌ Error insertando {casa_data.get('origen')}: {e}")
        return False


def insert_casas_batch(casas: List[Dict], fecha: str) -> Dict[str, int]:
    """
    Inserta múltiples casas de cambio en batch.
    
    Args:
        casas: Lista de casas scrapeadas
        fecha: Fecha en formato 'YYYY-MM-DD'
        
    Returns:
        Dict con contadores de insertados y omitidos
    """
    inserted = 0
    skipped = 0
    
    for casa in casas:
        casa_data = {
            "origen": casa["nombre"],
            "fecha": fecha,
            "precio_compra": casa["compra"],
            "precio_venta": casa["venta"],
        }
        
        if insert_casa_precio(casa_data):
            inserted += 1
        else:
            skipped += 1
    
    return {"inserted": inserted, "skipped": skipped}


def get_latest_casas_prices() -> List[Dict]:
    """
    Obtiene los precios más recientes de todas las casas.
    
    Returns:
        Lista de diccionarios con datos de casas
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("dolar")\
            .select("*")\
            .order("scraped_at", desc=True)\
            .limit(20)\
            .execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        print(f"❌ Error obteniendo precios: {e}")
        return []


def get_casas_by_date(fecha: str) -> List[Dict]:
    """
    Obtiene precios de casas para una fecha específica.
    
    Args:
        fecha: Fecha en formato 'YYYY-MM-DD'
        
    Returns:
        Lista de diccionarios con datos de casas
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("dolar")\
            .select("*")\
            .eq("fecha", fecha)\
            .execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        print(f"❌ Error obteniendo precios para {fecha}: {e}")
        return []


if __name__ == "__main__":
    # Prueba
    from datetime import datetime
    
    fecha = datetime.now().strftime("%Y-%m-%d")
    casas = get_casas_by_date(fecha)
    
    print(f"\n{'='*60}")
    print(f"Casas en DB para {fecha}: {len(casas)}")
    print(f"{'='*60}\n")
    
    for casa in casas[:5]:
        print(f"🏦 {casa.get('origen')}")
        print(f"   Compra: {casa.get('precio_compra')} | Venta: {casa.get('precio_venta')}\n")
