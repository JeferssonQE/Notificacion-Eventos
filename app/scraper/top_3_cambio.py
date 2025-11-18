import requests
import json
from bs4 import BeautifulSoup
from app.db.supabase.config import supabase
from datetime import datetime
CUANTOESTAELDOLAR_URL = "https://cuantoestaeldolar.pe/"

def time_today():
    now = datetime.now()
    fecha = f"{now.year}-{now.month:02d}-{now.day:02d}"
    return fecha

def insert_casa_db(data):
    response = supabase.table("dolar").insert(data).execute()
    return response

def get_exchange_rates_casas() -> list[dict]:

    response = requests.get(CUANTOESTAELDOLAR_URL, timeout=20)
    if response.status_code != 200:
        raise ConnectionError(f"Error HTTP {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    divs = soup.find_all(class_="ExchangeHouseItem_item_col__gudqq")

    casas = []
    for div in divs:
        # cada casa está dentro de un div.ExchangeHouseItem_item__FLx1C
        item = div.find("div", class_="ExchangeHouseItem_item__FLx1C")
        if not item:
            continue

        # URL y nombre (alt del <img>)
        enlace = item.find("a", href=True)
        img = item.find("img", alt=True)
        url = enlace["href"] if enlace else ""
        nombre = img["alt"].strip() if img else "Desconocido"

        # Valor de compra
        compra_tag = item.find("div", class_="ValueCurrency_content_buy__Z9pSf")
        compra = None
        if compra_tag:
            p = compra_tag.find("p")
            if p:
                try:
                    compra = float(p.text.strip())
                except ValueError:
                    compra = None
        # Valor de venta
        venta_tag = item.find("div", class_="ValueCurrency_content_sale__fdX_P")
        venta = None
        if venta_tag:
            p = venta_tag.find("p")
            if p:
                try:
                    venta = float(p.text.strip())
                except ValueError:
                    venta = None
        # Validar datos
        if compra is None or venta is None:
            continue
        if venta <= 0.0 or compra <= 0.0:
            continue

        casas.append({"nombre": nombre, "url": url, "compra": compra, "venta": venta})

        data={
            "origen": nombre,
            "fecha": time_today(),
            "precio_compra": compra,
            "precio_venta": venta,
        }

        insert_casa_db(data)
    
    return casas


import heapq


def top_3_mejores_casas(casas: list[dict]):

    top_3_compra = heapq.nlargest(3, casas, key=lambda x: x["compra"])
    top_3_venta = heapq.nsmallest(3, casas, key=lambda x: x["venta"])

    return top_3_compra, top_3_venta


def arbitraje_posible(casas: list[dict]) -> tuple[dict, dict, bool]:
    min_venta = min(casas, key=lambda x: x["venta"])
    max_compra = max(casas, key=lambda x: x["compra"])

    return min_venta, max_compra, max_compra["compra"] > min_venta["venta"]


if __name__ == "__main__":
    casas = get_exchange_rates_casas()
    min_v, max_c, posible = arbitraje_posible(casas)
    print("===========Hay arbitraje posible?=========\n Result : ", posible)
    print("Casa con menor precio de venta:")
    print(min_v)
    print("Casa con mayor precio de compra:")
    print(max_c)
    print("===========================================\n")
    tp3_c, tp3_v = top_3_mejores_casas(casas)

    print("Top 3 mejores casas para comprar dólares:")
    print(tp3_c)
    print("Top 3 mejores casas para vender dólares:")
    print(tp3_v)
