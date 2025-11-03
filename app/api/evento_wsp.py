import json
from fastapi import APIRouter, Request, HTTPException
from app.services.infrastructure.whatsapp.whatsapp_service import send_main_menu,send_whatsapp_template, send_whatsapp_text,send_whatsapp_buttons,send_whatsapp_list
from app.core.config import settings


router = APIRouter()
VERIFY_TOKEN = settings.VERIFY_TOKEN

# Verificación del webhook
@router.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return {"error": "Token inválido"}

@router.post("/webhook")
async def receive_webhook(request: Request):
    try:
        data = await request.json()
        print("📩 Mensaje entrante:", json.dumps(data, indent=2, ensure_ascii=False))

        entry = data["entry"][0]["changes"][0]["value"]
        messages = entry.get("messages")

        if messages:
            msg = messages[0]
            from_number = msg.get("from")
            text = msg.get("text", {}).get("body", "")

            if "interactive" in msg:
                interactive = msg["interactive"]

                # Caso: respuesta a LIST
                if interactive["type"] == "list_reply":
                    row_id = interactive["list_reply"]["id"]
                    return handle_action(from_number, row_id)
            
            result =send_main_menu(from_number)

            if "error" in result:
                raise HTTPException(status_code=400, detail=f"WhatsApp API error: {result['error']}")

            return {"status": "success", "data": result}

        return {"status": "no_message", "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando webhook: {str(e)}")


# 🚀 Enviar plantilla de alerta del dólar
@router.get("/send-dollar-alert/")
def send_template(
    to: str,
    movimiento: str = "subió",
    porcentaje: str = "2.5",
    valor: str = "3.79",
    fecha: str = "15/09/2025"
):
    try:
        result = send_whatsapp_template(to, movimiento, porcentaje, valor, fecha)

        if "error" in result:
            error_msg = result["error"].get("message", "Error desconocido")
            raise HTTPException(status_code=400, detail=f"WhatsApp API error: {error_msg}")

        return {"status": "success", "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando plantilla: {str(e)}")


def handle_action(to: str, action_id: str):
    if action_id == "ver_dolar":
        return send_whatsapp_text(to, "💵 El dólar hoy está en: 3.79 soles.")
    elif action_id == "alerta_dolar":
        return send_whatsapp_text(to, "📢 Función de alerta de dólar activada (demo).")
    elif action_id == "recordatorio":
        return send_whatsapp_text(to, "⏰ Aquí podrás crear recordatorios.")
    elif action_id == "facturador":
        return send_whatsapp_text(to, "🧾 Facturador SUNAT (en construcción).")
    elif action_id == "nosotros":
        return send_whatsapp_text(to, "ℹ️ Somos DólarBot, tu asistente financiero.")
    else:
        return send_whatsapp_text(to, f"⚠️ Opción no reconocida: {action_id}")
    

reply = (
                    "*📊 Resumen de alertas:*\n"
                    "Moneda   Cambio\n"
                    "USD      3.79\n"
                    "EUR      4.12\n"
                    "GBP      4.55"
                    )