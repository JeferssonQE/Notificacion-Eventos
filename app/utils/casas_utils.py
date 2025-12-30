"""
Utilidades para análisis de casas de cambio
"""
import heapq
from typing import List, Dict, Tuple


def get_top_3_compra(casas: List[Dict]) -> List[Dict]:
    """
    Obtiene las 3 mejores casas para comprar dólares (mayor precio de compra).
    
    Args:
        casas: Lista de casas con precios
        
    Returns:
        Top 3 casas con mejor precio de compra
    """
    return heapq.nlargest(3, casas, key=lambda x: x["compra"])


def get_top_3_venta(casas: List[Dict]) -> List[Dict]:
    """
    Obtiene las 3 mejores casas para vender dólares (menor precio de venta).
    
    Args:
        casas: Lista de casas con precios
        
    Returns:
        Top 3 casas con mejor precio de venta
    """
    return heapq.nsmallest(3, casas, key=lambda x: x["venta"])


def get_top_3_mejores_casas(casas: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Obtiene top 3 para comprar y vender.
    
    Args:
        casas: Lista de casas con precios
        
    Returns:
        Tupla (top_3_compra, top_3_venta)
    """
    return get_top_3_compra(casas), get_top_3_venta(casas)


def detectar_arbitraje(casas: List[Dict]) -> Dict:
    """
    Detecta si existe oportunidad de arbitraje.
    
    Args:
        casas: Lista de casas con precios
        
    Returns:
        Dict con información de arbitraje:
        {
            "posible": True/False,
            "comprar_en": {...},
            "vender_en": {...},
            "ganancia_por_dolar": 0.05
        }
    """
    if not casas:
        return {"posible": False}
    
    # Casa con menor precio de venta (mejor para comprar)
    mejor_compra = min(casas, key=lambda x: x["venta"])
    
    # Casa con mayor precio de compra (mejor para vender)
    mejor_venta = max(casas, key=lambda x: x["compra"])
    
    # Hay arbitraje si puedes comprar más barato de lo que vendes
    posible = mejor_venta["compra"] > mejor_compra["venta"]
    ganancia = mejor_venta["compra"] - mejor_compra["venta"] if posible else 0
    
    return {
        "posible": posible,
        "comprar_en": mejor_compra,
        "vender_en": mejor_venta,
        "ganancia_por_dolar": round(ganancia, 4)
    }


def calcular_spread(casa: Dict) -> float:
    """
    Calcula el spread (diferencia entre venta y compra).
    
    Args:
        casa: Dict con datos de la casa
        
    Returns:
        Spread calculado
    """
    return round(casa["venta"] - casa["compra"], 4)


def get_mejor_casa_compra(casas: List[Dict]) -> Dict:
    """
    Obtiene la mejor casa para comprar dólares.
    
    Args:
        casas: Lista de casas con precios
        
    Returns:
        Casa con menor precio de venta
    """
    return min(casas, key=lambda x: x["venta"])


def get_mejor_casa_venta(casas: List[Dict]) -> Dict:
    """
    Obtiene la mejor casa para vender dólares.
    
    Args:
        casas: Lista de casas con precios
        
    Returns:
        Casa con mayor precio de compra
    """
    return max(casas, key=lambda x: x["compra"])


if __name__ == "__main__":
    # Datos de ejemplo
    casas_ejemplo = [
        {"nombre": "Rextie", "compra": 3.75, "venta": 3.78, "url": ""},
        {"nombre": "Kambista", "compra": 3.76, "venta": 3.79, "url": ""},
        {"nombre": "Cambios Liberty", "compra": 3.74, "venta": 3.80, "url": ""},
    ]
    
    print("\n" + "="*60)
    print("ANÁLISIS DE CASAS DE CAMBIO")
    print("="*60 + "\n")
    
    # Top 3
    top_compra, top_venta = get_top_3_mejores_casas(casas_ejemplo)
    
    print("🏆 Top 3 para COMPRAR dólares:")
    for casa in top_compra:
        print(f"   {casa['nombre']}: {casa['compra']}")
    
    print("\n💰 Top 3 para VENDER dólares:")
    for casa in top_venta:
        print(f"   {casa['nombre']}: {casa['venta']}")
    
    # Arbitraje
    arbitraje = detectar_arbitraje(casas_ejemplo)
    print(f"\n🚀 Arbitraje posible: {arbitraje['posible']}")
    if arbitraje['posible']:
        print(f"   Comprar en: {arbitraje['comprar_en']['nombre']} a {arbitraje['comprar_en']['venta']}")
        print(f"   Vender en: {arbitraje['vender_en']['nombre']} a {arbitraje['vender_en']['compra']}")
        print(f"   Ganancia: S/ {arbitraje['ganancia_por_dolar']} por dólar")
    
    print("\n" + "="*60 + "\n")
