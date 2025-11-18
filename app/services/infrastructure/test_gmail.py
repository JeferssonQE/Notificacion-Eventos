from datetime import datetime
import os
from app.services.infrastructure.gmail.mailer import GmailMailer
from app.scraper.top_3_cambio import (
    get_exchange_rates_casas,
    top_3_mejores_casas,
    arbitraje_posible,
)
from app.core.config import settings
from app.scraper.get_sunat_dolar import dolar_sunat_today

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
    casas = get_exchange_rates_casas()
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

    # obtiene min_v (mejor venta), max_c (mejor compra), y si hay arbitraje posible
    min_v, max_c, posible = arbitraje_posible(casas)
    top3_c, top3_v = top_3_mejores_casas(casas)

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

    # Reemplazar valores en la plantilla
    html = (
        html.replace("{{fecha}}", datetime.now().strftime("%d/%m/%Y"))
        .replace("{{top3_compra}}", top3_compra_html)
        .replace("{{top3_venta}}", top3_venta_html)
        .replace("{{sunat_compra}}", f"{s_compra}")
        .replace("{{sunat_venta}}", f"{s_venta}")
        .replace("{{sunat_compra_var}}", sunat_compra_badge)
        .replace("{{sunat_venta_var}}", sunat_venta_badge)
        .replace("{{mejor_compra}}", f"{max_c['nombre']} ({max_c['compra']} PEN)")
        .replace("{{mejor_venta}}", f"{min_v['nombre']} ({min_v['venta']} PEN)")
        .replace("{{arbitraje_texto}}", arbitraje_txt)
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
