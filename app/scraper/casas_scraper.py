"""
Scraper de Casas de Cambio
Extrae datos de precios de cuantoestaeldolar.pe
"""
from typing import List, Dict
import requests
from bs4 import BeautifulSoup


CUANTOESTAELDOLAR_URL = "https://cuantoestaeldolar.pe/"


def scrape_casas_cambio() -> List[Dict]:
    """
    Extrae precios de todas las casas de cambio.
    
    Returns:
        Lista de diccionarios con datos de cada casa:
        [
            {
                "nombre": "Rextie",
                "url": "https://...",
                "compra": 3.75,
                "venta": 3.78
            },
            ...
        ]
    """
    try:
        response = requests.get(CUANTOESTAELDOLAR_URL, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error al conectar con {CUANTOESTAELDOLAR_URL}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all(class_="ExchangeHouseItem_item_col__gudqq")
    
    casas = []
    
    for div in divs:
        item = div.find("div", class_="ExchangeHouseItem_item__FLx1C")
        if not item:
            continue
        
        # Extraer datos
        casa_data = _extract_casa_data(item)
        
        # Validar datos
        if _is_valid_casa(casa_data):
            casas.append(casa_data)
    
    print(f"✅ Scrapeadas {len(casas)} casas de cambio")
    return casas


def _extract_casa_data(item) -> Dict:
    """
    Extrae datos de un elemento HTML de casa de cambio.
    
    Args:
        item: Elemento BeautifulSoup
        
    Returns:
        Dict con datos de la casa
    """
    # URL y nombre
    enlace = item.find("a", href=True)
    img = item.find("img", alt=True)
    url = enlace["href"] if enlace else ""
    nombre = img["alt"].strip() if img else "Desconocido"
    
    # Precio de compra
    compra = None
    compra_tag = item.find("div", class_="ValueCurrency_content_buy__Z9pSf")
    if compra_tag:
        p = compra_tag.find("p")
        if p:
            try:
                compra = float(p.text.strip())
            except ValueError:
                pass
    
    # Precio de venta
    venta = None
    venta_tag = item.find("div", class_="ValueCurrency_content_sale__fdX_P")
    if venta_tag:
        p = venta_tag.find("p")
        if p:
            try:
                venta = float(p.text.strip())
            except ValueError:
                pass
    
    return {
        "nombre": nombre,
        "url": url,
        "compra": compra,
        "venta": venta
    }


def _is_valid_casa(casa: Dict) -> bool:
    """
    Valida que los datos de una casa sean correctos.
    
    Args:
        casa: Dict con datos de la casa
        
    Returns:
        True si los datos son válidos
    """
    compra = casa.get("compra")
    venta = casa.get("venta")
    
    if compra is None or venta is None:
        return False
    
    if compra <= 0.0 or venta <= 0.0:
        return False
    
    return True


if __name__ == "__main__":
    casas = scrape_casas_cambio()
    
    print(f"\n{'='*60}")
    print(f"Casas scrapeadas: {len(casas)}")
    print(f"{'='*60}\n")
    
    for casa in casas[:5]:  # Mostrar primeras 5
        print(f"🏦 {casa['nombre']}")
        print(f"   Compra: {casa['compra']} | Venta: {casa['venta']}")
        print(f"   URL: {casa['url']}\n")
