import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc
from bs4 import BeautifulSoup

import time
#SELENIUM 
TKAMBIO_URL = "https://tkambio.com/?gad_source=1&gad_campaignid=17557936036&gbraid=0AAAAACn9oC-oQZQZR0qR1oHnPIEEoiBEN&gclid=CjwKCAjwlOrFBhBaEiwAw4bYDe1tFs5M2TPyEAQb4sgA2_yYao4EJntVAKC-B6Yz7xbBN4H_4Wwy-hoCRVYQAvD_BwE#gad_source_1"
SUNAT_URL = "https://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias"

SOURCE_URL = "https://cuantoestaeldolar.pe/"
SUNAT_DOLAR_TODAY="https://www.sunat.gob.pe/"

def config_driver():

    options = uc.ChromeOptions()
    options.headless = False   # Si quieres ver el navegador, usa False

    # Opciones anti-detección
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)
    return driver

def get_html_with_selenium(url: str) -> str:
    driver= config_driver()

    try:
        driver.get(url)

        # Espera hasta que algún <span class="price"> tenga texto dentro
        WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "span.price").text.strip() != ""
        )

        html = driver.page_source
        return html
    finally:
        time.sleep(2)  # opcional: para ver el navegador un momento
        driver.quit()


def extract_dolar_value_tkambio(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    compra_span = soup.select_one(
        "#row-hero div:nth-of-type(2) div:nth-of-type(1) div:nth-of-type(1) "
        "div:nth-of-type(2) div div:nth-of-type(1) div p:nth-of-type(3) span"
    )
    venta_span = soup.select_one(
        "#row-hero div:nth-of-type(2) div:nth-of-type(1) div:nth-of-type(1) "
        "div:nth-of-type(2) div div:nth-of-type(2) div p:nth-of-type(3) span"
    )
    print("[Debug] compra_span:", compra_span, "venta_span:", venta_span)  # Debugging line
    if compra_span and venta_span:
        try:
            valor_compra = float(compra_span.text.strip())
            valor_venta = float(venta_span.text.strip())
            return {"compra": valor_compra, "venta": valor_venta}
        except Exception as e:
            raise ValueError(f"Error al extraer valores: {e}")
    else:
        raise ValueError("No se encontraron elementos para compra/venta.")


# Ejemplo
html = get_html_with_selenium(SOURCE_URL)
print(html)
