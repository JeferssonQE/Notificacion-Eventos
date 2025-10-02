from celery import Celery
from app.core.config import settings
from celery.schedules import crontab

celery_app = Celery(
    "dolar_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.timezone = "America/Lima"
celery_app.conf.task_track_started = True
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]

# Programación con Beat
celery_app.conf.beat_schedule = {
    # a) Scraping diario a las 00:32 (Lima). Usa el wrapper con jitter.
    "scraper-diario-0032": {
        "task": "app.utils.tasks.scrape_and_save_with_jitter",
        "schedule": crontab(minute=32, hour=0),
        "args": (180,),  # jitter máx 180s (3 min). Cambia a 0 si no quieres jitter.
    },

    # b) Verificar alertas a las 08:00 (Lima)
    "verificar-alertas-0800": {
        "task": "app.utils.tasks.verificar_alertas_job",
        "schedule": crontab(minute=0, hour=8),
    },
}