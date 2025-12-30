import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_international_data(start_date: str, end_date: str):
    """
    Obtiene datos de Yahoo Finance.
    Tickers:
    - HG=F: Futuros de Cobre (High Grade Copper) - Vital para Perú
    - DX-Y.NYB: Índice Dólar (DXY) - Vital para tendencia global
    """
    
    # Nota: yfinance el 'end_date' es exclusivo, así que sumamos 1 día para asegurar
    # que traiga la data hasta la fecha final solicitada.
    end_dt_obj = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    adjusted_end = end_dt_obj.strftime("%Y-%m-%d")

    tickers = ["HG=F", "DX-Y.NYB"]
    
    print(f"Fetching Yahoo Finance: {tickers} from {start_date} to {end_date}")
    
    try:
        # Descargamos la data
        data = yf.download(tickers, start=start_date, end=adjusted_end, progress=False)
        
        # Yahoo devuelve un DataFrame MultiIndex. Nos interesa solo el precio de Cierre ('Close')
        df_close = data['Close']
        
        records = []
        
        # Iteramos por las fechas
        for index, row in df_close.iterrows():
            # Convertir Timestamp a string
            fecha_str = index.strftime('%Y-%m-%d')
            
            # Extraer valores (Manejando posibles NaNs si un mercado cerró y el otro no)
            cobre_val = row.get('HG=F')
            dxy_val = row.get('DX-Y.NYB')
            
            # Solo agregamos si tenemos al menos un dato válido
            if pd.notna(cobre_val) or pd.notna(dxy_val):
                record = {
                    "fecha": fecha_str,
                    "precio_cobre": round(float(cobre_val), 4) if pd.notna(cobre_val) else None,
                    "indice_dxy": round(float(dxy_val), 4) if pd.notna(dxy_val) else None,
                    "origen": "YAHOO"
                }
                records.append(record)
                
        return records

    except Exception as e:
        print(f"❌ Error en Yahoo Finance Service: {e}")
        return []

# --- PRUEBA RÁPIDA ---
if __name__ == "__main__":
    # Probamos con las mismas fechas que tu BCRP
    data = get_international_data("2025-12-18", "2025-12-24")
    print(data)