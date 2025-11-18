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
    return supabase.table("dolar").insert(data).execute()

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
    response = requests.post(URL, json=payload, headers=headers)

    if not response.ok:
        print("❌ Error SUNAT:", response.status_code)
        return None

    compra = venta = 0.0

    for item in response.json():
        if item["fecPublica"] == fecha_sunat:
            if item["codTipo"] == "C":
                compra = float(item["valTipo"])
            elif item["codTipo"] == "V":
                venta = float(item["valTipo"])

    # No se encontró datos del día
    if compra == 0 and venta == 0:
        print("❌ SUNAT no publicó tipo de cambio hoy")
        return None

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

if __name__ == "__main__":
    data = dolar_sunat_today()
    print(data)
