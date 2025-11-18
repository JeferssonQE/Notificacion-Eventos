import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


class GmailMailer:
    def __init__(self):
        self.email_user = settings.EMAIL_USER
        self.email_pass = settings.EMAIL_PASS
        if not self.email_user or not self.email_pass:
            raise ValueError(
                "❌ Faltan las variables EMAIL_USER o EMAIL_PASS en el entorno."
            )

    def send_html_email(self, to_email: str, subject: str, html_content: str):
        msg = MIMEMultipart("alternative")
        msg["From"] = self.email_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            print("✅ Correo enviado con éxito.")
        except Exception as e:
            print("❌ Error enviando correo:", e)
