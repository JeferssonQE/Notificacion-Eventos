import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict

# Configuración
BASE_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
FORMAT = "json"

# Mapeo de meses en español (La API devuelve "Ene", "Feb", etc.)
MONTH_MAP = {
    "Ene": "01", "Feb": "02", "Mar": "03", "Abr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Ago": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dic": "12"
}

def parse_bcrp_date(date_str: str) -> str:
    """
    Convierte fechas del BCRP (ej: '24.Dic.25') a formato SQL (ej: '2025-12-24')
    """
    try:
        # Formato esperado: DD.MMM.YY (ej: 24.Dic.25)
        parts = date_str.split('.')
        if len(parts) != 3:
            return None
        
        day = parts[0].zfill(2)
        month_str = parts[1].capitalize()
        year = "20" + parts[2] # Asumimos siglo 21
        
        month_num = MONTH_MAP.get(month_str)
        
        if month_num:
            return f"{year}-{month_num}-{day}"
        return None
    except Exception as e:
        print(f"Error parsing date {date_str}: {e}")
        return None

def get_bcrp_data(start_date: str, end_date: str) -> List[Dict]:
    """
    Consulta la API del BCRP.
    start_date y end_date deben ser 'YYYY-MM-DD'
    """
    # Códigos: TC Venta Interbancario (PD04640PD) y Tasa Interbancaria (PD04639PD)
    series = "PD04640PD-PD04639PD"
    
    # Construcción de URL según documentación (Página 3)
    url = f"{BASE_URL}/{series}/{FORMAT}/{start_date}/{end_date}"
    
    print(f"Fetching BCRP: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        records = []
        
        # La API devuelve una lista de 'periods'
        if 'periods' in data:
            for period in data['periods']:
                # period['name'] es la fecha (ej: 24.Dic.25)
                # period['values'] es una lista con los valores de las series pedidas
                
                fecha_sql = parse_bcrp_date(period['name'])
                
                if fecha_sql:
                    tc_venta = period['values'][0]
                    tasa_interbancaria = period['values'][1]
                    
                    # Validar que no sean "n.d." (no disponible)
                    record = {
                        "fecha": fecha_sql,
                        "tc_interbancario_venta": float(tc_venta) if tc_venta != "n.d." else None,
                        "tasa_interbancaria": float(tasa_interbancaria) if tasa_interbancaria != "n.d." else None,
                        "origen": "BCRP_API"
                    }
                    records.append(record)
                    
        return records

    except Exception as e:
        print(f"Error en BCRP Service: {e}")
        return []

# --- PRUEBA RÁPIDA ---
if __name__ == "__main__":
    # Probamos traer la última semana
    data = get_bcrp_data("2025-12-18", "2025-12-24")
    print(data)