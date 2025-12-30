from datetime import datetime
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.infrastructure.gmail.mailer import GmailMailer
from app.scraper.casas_scraper import scrape_casas_cambio
from app.utils.casas_utils import (
    get_top_3_mejores_casas,
    detectar_arbitraje,
)
from app.core.config import settings
from app.scraper.get_sunat_dolar import dolar_sunat_today

# Importar análisis estratégico
try:
    from app.analytics.daily_report import generate_daily_insights, format_insights_for_email
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    print("⚠️ Módulo de analytics no disponible, usando reporte básico")

def porcentaje_cambio(actual, anterior):
    try:
        return round(((actual - anterior) / anterior) * 100, 2)
    except ZeroDivisionError:
        return 0
def badge(valor):
    """Devuelve un badge HTML de variación"""
    if valor > 0:
        return f"<span style='color:#059669;'>▲ {valor}%</span>"
    elif valor < 0:
        return f"<span style='color:#dc2626;'>▼ {abs(valor)}%</span>"
    else:
        return "<span style='color:#6b7280;'>• 0%</span>"

def send_gmail_with_dolar():
    casas = scrape_casas_cambio()
    if not casas:
        print("❌ No se pudieron obtener las casas de cambio.")
        return

    # referencia Sunat
    s_data   = dolar_sunat_today()
    s_compra = s_data["compra"]
    s_venta  = s_data["venta"]

    # Variación SUNAT
    sunat_compra_var = 0
    sunat_venta_var  = 0
    if s_data.get("ayer"):
        sunat_compra_var = porcentaje_cambio(s_compra, s_data["ayer"]["compra"])
        sunat_venta_var  = porcentaje_cambio(s_venta, s_data["ayer"]["venta"])

    sunat_compra_badge = badge(sunat_compra_var)
    sunat_venta_badge  = badge(sunat_venta_var)

    # Análisis de casas
    arbitraje = detectar_arbitraje(casas)
    top3_c, top3_v = get_top_3_mejores_casas(casas)
    
    # Extraer datos de arbitraje
    posible = arbitraje["posible"]
    min_v = arbitraje.get("comprar_en", {})
    max_c = arbitraje.get("vender_en", {})

    # Cargar plantilla HTML base
    template_path = os.path.join(
        os.path.dirname(__file__), "gmail", "reporte_casas.html"
    )
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # === Construir secciones dinámicas ===
    top3_compra_html = "".join(
        [
            f"<li style='margin-bottom:4px;'>🏦 "
            f"<a href='{casa['url']}' style='color:#0077cc;text-decoration:none;' target='_blank'>{casa['nombre']}</a>: "
            f"<b style='color:#00b341'>{casa['compra']}</b> PEN</li>"
            for casa in top3_c
        ]
    )

    top3_venta_html = "".join(
        [
            f"<li style='margin-bottom:4px;'>💰 "
            f"<a href='{casa['url']}' style='color:#0077cc;text-decoration:none;' target='_blank'>{casa['nombre']}</a>: "
            f"<b style='color:#e63946'>{casa['venta']}</b> PEN</li>"
            for casa in top3_v
        ]
    )

    arbitraje_txt = (
        "✅ Existe oportunidad de arbitraje"
        if posible
        else "❌ No hay arbitraje disponible"
    )
    
    # === Generar insights estratégicos ===
    insights_html = ""
    if ANALYTICS_AVAILABLE:
        try:
            print("📊 Generando análisis estratégico...")
            insights = generate_daily_insights()
            insights_html = format_insights_for_email(insights)
            print("✅ Análisis estratégico generado")
        except Exception as e:
            print(f"⚠️ Error generando insights: {e}")
            insights_html = ""

    # Reemplazar valores en la plantilla
    html = (
        html.replace("{{fecha}}", datetime.now().strftime("%d/%m/%Y"))
        .replace("{{top3_compra}}", top3_compra_html)
        .replace("{{top3_venta}}", top3_venta_html)
        .replace("{{sunat_compra}}", f"{s_compra}")
        .replace("{{sunat_venta}}", f"{s_venta}")
        .replace("{{sunat_compra_var}}", sunat_compra_badge)
        .replace("{{sunat_venta_var}}", sunat_venta_badge)
        .replace("{{mejor_compra}}", f"{max_c.get('nombre', 'N/A')} ({max_c.get('compra', 0)} PEN)")
        .replace("{{mejor_venta}}", f"{min_v.get('nombre', 'N/A')} ({min_v.get('venta', 0)} PEN)")
        .replace("{{arbitraje_texto}}", arbitraje_txt)
        .replace("{{insights_estrategicos}}", insights_html)
    )

    # === Enviar correo ===
    subject = (
        f"📩 Informe diario de casas de cambio - {datetime.now().strftime('%d/%m/%Y')}"
    )
    mailer = GmailMailer()
    mailer.send_html_email(
        to_email=settings.EMAIL_TO, subject=subject, html_content=html
    )


if __name__ == "__main__":
    send_gmail_with_dolar()
