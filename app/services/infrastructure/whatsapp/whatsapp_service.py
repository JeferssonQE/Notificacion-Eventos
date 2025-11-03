import requests
import os
import dotenv

dotenv.load_dotenv()

ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN") 
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID") 

GRAPH_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"


def send_whatsapp_text(to: str, text: str):
    """
    Envia un mensaje de texto simple a WhatsApp
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(GRAPH_URL, headers=headers, json=data)
    return response.json()


def send_whatsapp_template(to: str, nombre:str,movimiento: str, porcentaje: str, valor: str, fecha: str):
    """
    Envia un mensaje usando la plantilla activa `recordatorio_evento`
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": "recordatorio_evento",
            "language": {"code": "es"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": nombre},      # {{1}}
                        {"type": "text", "text": movimiento},   # {{2}}
                        {"type": "text", "text": porcentaje},  # {{3}}
                        {"type": "text", "text": valor},       # {{4}}
                        {"type": "text", "text": fecha}        # {{5}}
                    ]
                }
            ]
        }
    }
    response = requests.post(GRAPH_URL, headers=headers, json=data)
    return response.json()

#Templates disponibles:
def send_whatsapp_list(to: str):
    """
    Envía un mensaje tipo LIST (ideal para mostrar varias opciones estilo tabla).
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {"type": "text", "text": "💱 Tipos de cambio"},
            "body": {"text": "Selecciona una moneda:"},
            "footer": {"text": "Actualizado hoy"},
            "action": {
                "button": "Ver opciones",
                "sections": [
                    {
                        "title": "Monedas",
                        "rows": [
                            {"id": "usd", "title": "USD", "description": "3.79"},
                            {"id": "eur", "title": "EUR", "description": "4.12"},
                            {"id": "gbp", "title": "GBP", "description": "4.55"}
                        ]
                    }
                ]
            }
        }
    }
    return requests.post(GRAPH_URL, headers=headers, json=data).json()

def send_whatsapp_buttons(to: str):
    """
    Envía un mensaje tipo BUTTON (ideal para pocas opciones rápidas).
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "Elige una moneda 💵"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "usd", "title": "USD 3.79"}},
                    {"type": "reply", "reply": {"id": "eur", "title": "EUR 4.12"}},
                    {"type": "reply", "reply": {"id": "gbp", "title": "GBP 4.55"}}
                ]
            }
        }
    }
    return requests.post(GRAPH_URL, headers=headers, json=data).json()

def send_main_menu(to: str):
    """
    Envía el menú principal del asistente usando LIST (puede tener más de 3 opciones).
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {"type": "text", "text": "🤖 Menú principal"},
            "body": {"text": "👋 Bienvenido al asistente DólarBot\nElige una opción:"},
            "footer": {"text": "Powered by FastAPI"},
            "action": {
                "button": "Ver opciones",
                "sections": [
                    {
                        "title": "Opciones disponibles",
                        "rows": [
                            {"id": "ver_dolar", "title": "💵 Ver dólar hoy", "description": "Consulta el tipo de cambio actual"},
                            {"id": "alerta_dolar", "title": "📢 Activar alerta", "description": "Configura una alerta personalizada"},
                            {"id": "recordatorio", "title": "⏰ Crear recordatorio", "description": "Recibe recordatorios automáticos"},
                            {"id": "facturador", "title": "🧾 Facturador SUNAT", "description": "Envío de facturas y boletas"},
                            {"id": "alerta_apuestas", "title": "🎲 Alerta de apuestas", "description": "Recibe alertas de apuestas deportivas"},
                            {"id": "nosotros", "title": "ℹ️ Sobre nosotros", "description": "Información del asistente"},
                        ]
                    }
                ]
            }
        }
    }

    return requests.post(GRAPH_URL, headers=headers, json=data).json()
    