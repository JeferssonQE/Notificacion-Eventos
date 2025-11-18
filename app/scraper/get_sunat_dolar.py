import requests
from app.core.config import settings
from app.db.supabase.config import supabase
from datetime import datetime

url = "https://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias/listarTipoCambio"

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
    response = supabase.table("dolar").insert(data).execute()
    return response

def dolar_sunat_today():
    year, month, day = time_today()
    print(f"📅 Consultando tipo de cambio para {day}/{month}/{year}...")
    payload = {"anio": year, "mes": month - 1, "token": settings.TOKEN_SUNAT_API}

    response = requests.post(url, json=payload, headers=headers)

    origen = "SUNAT_API"
    fecha = f"{day:02d}/{month:02d}/{year}"
    compra = 0.0
    venta = 0.0
    if response.ok:
        print("✅ Respuesta recibida: \nlen(response): " + str(len(response.json())))

        for item in response.json():
            if item["fecPublica"] == fecha:
                if item["codTipo"] == "V":
                    venta = float(item["valTipo"])
                if item["codTipo"] == "C":
                    compra = float(item["valTipo"])
        data={
            "origen": origen,
            "fecha": f"{year}-{month:02d}-{day:02d}",
            "precio_compra": compra,
            "precio_venta": venta,
        }
        insert_db(data)
        
        return {"origen": origen, "fecha": fecha, "compra": compra, "venta": venta}
    else:
        print("❌ Error:", response.status_code, response.text)
    return None


if __name__ == "__main__":
    data = dolar_sunat_today()
    print(data)
