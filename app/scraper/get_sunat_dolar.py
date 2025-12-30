import requests
from app.core.config import settings
from app.db.supabase.config import supabase
from datetime import datetime

URL = "https://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias/listarTipoCambio"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/141.0.0.0 Safari/537.36",
}


def time_today():
    now = datetime.now()
    return now.year, now.month, now.day

def insert_db(data):
    try:
        #validate already data of dolar exists 
        fecha = data.get("fecha")
        existing = supabase.table("dolar").select("*").eq("origen", data.get("origen")).eq("fecha", fecha).execute()
        if existing.data:
            print(f"Data for {data.get('origen')} on {fecha} already exists. Skipping insert.")
            return existing
        return supabase.table("dolar").insert(data).execute()
    except Exception as e:
        print("❌ Error inserting data:", e)
        return None
    
def get_history(origen):
    return (
        supabase.table("dolar")
        .select("*")
        .eq("origen", origen)
        .order("fecha", desc=True)
        .execute()
        .data
    )

def dolar_sunat_today():
    today = datetime.now()
    fecha_iso = today.strftime("%Y-%m-%d")
    fecha_sunat = today.strftime("%d/%m/%Y")

    payload = {"anio": today.year, "mes": today.month - 1, "token": settings.TOKEN_SUNAT_API}
    
    try:
        response = requests.post(URL, json=payload, headers=headers, timeout=10)
        
        if not response.ok:
            print(f"⚠️ Error API SUNAT: {response.status_code}")
            print("🔄 Intentando con scraper como fallback...")
            return _dolar_sunat_scraper_fallback()

        compra = venta = 0.0

        for item in response.json():
            if item["fecPublica"] == fecha_sunat:
                if item["codTipo"] == "C":
                    compra = float(item["valTipo"])
                elif item["codTipo"] == "V":
                    venta = float(item["valTipo"])

        # No se encontró datos del día
        if compra == 0 and venta == 0:
            print("⚠️ SUNAT API no tiene datos para hoy (fin de semana/feriado)")
            print("🔄 Intentando con scraper como fallback...")
            return _dolar_sunat_scraper_fallback()

        # Obtener historial antes de insertar
        history = get_history("SUNAT_API")

        # Si ya existe el registro de hoy → no insertar
        if history and history[0]["fecha"] == fecha_iso:
            print("⚠️ Ya existe registro de hoy. No se inserta.")
        else:
            insert_db({
                "origen": "SUNAT_API",
                "fecha": fecha_iso,
                "precio_compra": compra,
                "precio_venta": venta,
            })

        # Actualizamos historia después de insertar
        history = get_history("SUNAT_API")

        # Encontrar ayer
        ayer = None
        if len(history) > 1:
            ayer = {
                "compra": history[1]["precio_compra"],
                "venta": history[1]["precio_venta"],
                "fecha": history[1]["fecha"],
            }

        return {
            "origen": "SUNAT_API",
            "fecha": fecha_iso,
            "compra": compra,
            "venta": venta,
            "ayer": ayer,
        }
    
    except Exception as e:
        print(f"❌ Error al consultar API SUNAT: {e}")
        print("🔄 Intentando con scraper como fallback...")
        return _dolar_sunat_scraper_fallback()


def _dolar_sunat_scraper_fallback():
    """
    Fallback usando scraper cuando la API falla o no tiene datos
    """
    try:
        from app.scraper.scraper_sunat_dolar import get_today_exchange_rate
        
        print("🌐 Ejecutando scraper de SUNAT...")
        scraper_data = get_today_exchange_rate()
        
        if not scraper_data:
            print("❌ Scraper tampoco pudo obtener datos")
            return None
        
        # Convertir formato del scraper al formato esperado
        fecha_iso = datetime.now().strftime("%Y-%m-%d")
        compra = scraper_data.get("precio_compra")
        venta = scraper_data.get("precio_venta")
        
        if not compra or not venta:
            print("❌ Scraper no devolvió datos válidos")
            return None
        
        # Obtener historial
        history = get_history("SUNAT_SCRAPER")
        
        # Si ya existe el registro → no insertar
        if history and history[0]["fecha"] == fecha_iso:
            print("⚠️ Ya existe registro de scraper para hoy. No se inserta.")
        else:
            insert_db({
                "origen": "SUNAT_SCRAPER",
                "fecha": fecha_iso,
                "precio_compra": compra,
                "precio_venta": venta,
            })
        
        # Actualizar historia
        history = get_history("SUNAT_SCRAPER")
        
        # Encontrar ayer
        ayer = None
        if len(history) > 1:
            ayer = {
                "compra": history[1]["precio_compra"],
                "venta": history[1]["precio_venta"],
                "fecha": history[1]["fecha"],
            }
        
        print(f"✅ Scraper exitoso: Compra {compra}, Venta {venta}")
        
        return {
            "origen": "SUNAT_SCRAPER",
            "fecha": fecha_iso,
            "compra": compra,
            "venta": venta,
            "ayer": ayer,
        }
    
    except Exception as e:
        print(f"❌ Error en scraper fallback: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    data = dolar_sunat_today()
    print(data)
