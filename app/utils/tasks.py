from datetime import datetime
from app.scraper.scraper_dolar import get_today_exchange_rate
from app.db.database import Dolar, get_db_session
from app.utils.send_celery import celery_app

@celery_app.task
def run_scraper_and_save():
    session = get_db_session()()
    data = get_today_exchange_rate()
    if not data:
        return "❌ No se pudo obtener datos"

    fecha = datetime.strptime(data["fecha"], "%d").date().replace(
        year=datetime.today().year, month=datetime.today().month
    )

    dolar = Dolar(
        origen=data["origen"],
        fecha=fecha,
        precio_compra=data["compra"],
        precio_venta=data["venta"],
        diferencia_ayer=None
    )

    session.merge(dolar)
    session.commit()
    session.close()
    return f"✅ Guardado {fecha}: C={dolar.precio_compra}, V={dolar.precio_venta}"
