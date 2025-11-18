import time, random
from app.celery.config import celery_app
from app.utils.get_sunat_dolar import dolar_sunat_today

# from app.scraper.scraper_dolar import get_today_exchange_rate
from app.db.database import get_db_session, Dolar
from app.db.database import RecordatorioDolar
from celery.schedules import crontab


# test celery
@celery_app.task(name="tasks.prueba")
def prueba():
    print("✅ Celery está funcionando correctamente")


# ----- GUARDAR PRECIO -----
@celery_app.task
def update_dolar_price(origen, fecha, precio_venta, precio_compra):
    session = get_db_session()()
    try:
        dolar = Dolar(
            origen=origen,
            fecha=fecha,
            precio_venta=precio_venta,
            precio_compra=precio_compra,
        )
        session.merge(dolar)
        session.commit()
        return f"✅ Guardado {fecha}: C={dolar.precio_compra}, V={dolar.precio_venta}"
    except Exception as e:
        session.rollback()
        return f"❌ Error guardando: {e}"
    finally:
        session.close()


# ----- SCRAPE + SAVE -----
@celery_app.task
def scrape_and_save():
    data = dolar_sunat_today()
    if not data:
        return "❌ No se pudo obtener datos de SUNAT"

    return update_dolar_price(
        "SUNAT_API",
        data["fecha"],
        data["venta"],
        data["compra"],
    )


# Wrapper con jitter para no golpear siempre exacto a las 00:32
@celery_app.task(name="app.utils.tasks.scrape_and_save_with_jitter")
def scrape_and_save_with_jitter(jitter_max_seconds=180):
    if jitter_max_seconds and jitter_max_seconds > 0:
        time.sleep(random.randint(0, int(jitter_max_seconds)))
    return scrape_and_save()


# ----- ALERTAS -----
def calculate_increment(current, percentage):
    return current + (current * (percentage / 100.0))


def calculate_decrement(current, percentage):
    return current - (current * (percentage / 100.0))


@celery_app.task(name="app.utils.tasks.verificar_alertas")
def verificar_alertas(precio_actual):
    session = get_db_session()()
    print(f"🔔 Verificando alertas para precio actual: {precio_actual}")
    try:
        alertas = session.query(RecordatorioDolar).filter_by(activo=True).all()
        disparadas = 0

        for alerta in alertas:
            if alerta.movimiento == "subio" and precio_actual >= calculate_increment(
                alerta.valor_objetivo, alerta.porcentaje
            ):
                enviar_notificacion.delay(
                    alerta.user_id, precio_actual, alerta.valor_objetivo, "subio"
                )
                alerta.activo = False
                disparadas += 1
            elif alerta.movimiento == "bajo" and precio_actual <= calculate_decrement(
                alerta.valor_objetivo, alerta.porcentaje
            ):
                enviar_notificacion.delay(
                    alerta.user_id, precio_actual, alerta.valor_objetivo, "bajo"
                )
                alerta.activo = False
                disparadas += 1
        session.commit()
        return f"🔔 Alertas disparadas: {disparadas}"
    except Exception as e:
        session.rollback()
        return f"❌ Error verificando alertas: {e}"
    finally:
        session.close()


@celery_app.task
def enviar_notificacion(user_id, precio, objetivo, movimiento):
    # Aquí integras correo/WhatsApp/SMS/push, etc.
    print(
        f"📩 Notificación → user={user_id} | precio={precio} | objetivo={objetivo} | movimiento={movimiento}"
    )
