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
    return webdriver.Chrome(service=Service(ruta), options=options)


def extract_number(texto):
    try:
        return float(re.search(r"\d+\.\d+", texto).group())
    except:
        return None


def get_today_exchange_rate():
    driver = setup_driver()
    driver.get(URL_SUNAT)

    try:
        # Esperar a que cargue la celda de hoy con el precio de venta
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "td.calendar-day.today.current .event.pap-all-day")
            )
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        today_cell = soup.select_one("td.calendar-day.today.current")

        if today_cell:
            fecha_elem = today_cell.find("div", class_="date")
            compra_elem = today_cell.find(
                "div", class_=lambda c: c and "normal-all-day" in c
            )
            venta_elem = today_cell.find(
                "div", class_=lambda c: c and "pap-all-day" in c
            )

            fecha = fecha_elem.text.strip() if fecha_elem else "?"
            compra = extract_number(compra_elem.text) if compra_elem else None
            venta = extract_number(venta_elem.text) if venta_elem else None

            return {
                "origen": "SUNAT",
                "fecha": fecha,
                "precio_compra": compra,
                "precio_venta": venta,
            }
        else:
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
