from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64, os

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CREDENTIALS_API = r"C:\Users\jefersson\Desktop\dolar\app\services\infrastructure\credentials.json"

def enviar_con_gmail_api():
    # Autenticación local la primera vez
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_API, SCOPES)
        creds = flow.run_local_server(port=8080) # eleigr uno fijo, en uri
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    msg = MIMEText("¡Hola! Este correo se envió automáticamente 😎")
    msg["to"] = "tu_correo@gmail.com"
    msg["subject"] = "Reporte diario"
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()

if __name__ == "__main__":
    enviar_con_gmail_api()
    print("Correo enviado con éxito.")