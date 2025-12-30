from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time

URL_SUNAT = "https://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias"


def setup_driver():
    ruta = ChromeDriverManager().install()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # comenta esta línea si quieres ver el navegador
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(service=Service(ruta), options=options)


def extract_number(texto):
    try:
        # Buscar cualquier número decimal en el texto
        match = re.search(r"\d+\.\d+", texto)
        if match:
            return float(match.group())
        return None
    except:
        return None


def get_today_exchange_rate():
    driver = setup_driver()
    
    try:
        print("⏳ Cargando página de SUNAT...")
        driver.get(URL_SUNAT)
        
        # Esperar a que la página cargue completamente
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        print("🔍 Buscando tipo de cambio...")
        
        # Buscar la celda de hoy primero
        today_cell = soup.select_one("td.today")
        
        if today_cell:
            print(f"✅ Celda de hoy encontrada")
            
            # Verificar si tiene datos
            compra_elem = today_cell.find("div", class_=lambda c: c and "normal-all-day" in c)
            venta_elem = today_cell.find("div", class_=lambda c: c and "pap-all-day" in c)
            
            if compra_elem and venta_elem:
                fecha_elem = today_cell.find("div", class_="date")
                fecha = fecha_elem.text.strip() if fecha_elem else "?"
                compra = extract_number(compra_elem.text)
                venta = extract_number(venta_elem.text)
                
                print(f"📅 Fecha: {fecha}")
                print(f"💵 Compra: {compra}")
                print(f"💰 Venta: {venta}")
                
                return {
                    "origen": "SUNAT",
                    "fecha": fecha,
                    "precio_compra": compra,
                    "precio_venta": venta,
                }
            else:
                print("⚠️  Hoy no hay datos (fin de semana o feriado)")
                print("🔍 Buscando el último día con datos disponibles...")
        
        # Si hoy no tiene datos, buscar el último día con datos
        all_cells = soup.select("td.calendar-day.current")
        
        # Recorrer desde el final hacia atrás
        for cell in reversed(all_cells):
            compra_elem = cell.find("div", class_=lambda c: c and "normal-all-day" in c)
            venta_elem = cell.find("div", class_=lambda c: c and "pap-all-day" in c)
            
            if compra_elem and venta_elem:
                fecha_elem = cell.find("div", class_="date")
                fecha = fecha_elem.text.strip() if fecha_elem else "?"
                compra = extract_number(compra_elem.text)
                venta = extract_number(venta_elem.text)
                
                print(f"✅ Último día con datos encontrado")
                print(f"📅 Fecha: {fecha}")
                print(f"💵 Compra: {compra}")
                print(f"💰 Venta: {venta}")
                
                return {
                    "origen": "SUNAT",
                    "fecha": fecha,
                    "precio_compra": compra,
                    "precio_venta": venta,
                }
        
        print("❌ No se encontraron datos de tipo de cambio")
        return None

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        driver.quit()


if __name__ == "__main__":
    dolar_hoy = get_today_exchange_rate()
    if dolar_hoy:
        print("TEST : DOLAR SUNAT")
        print(dolar_hoy)
    else:
        print("❌ No se pudo obtener el tipo de cambio de hoy.")
