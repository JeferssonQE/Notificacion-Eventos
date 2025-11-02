from celery import Celery
from app.core.config import settings


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
celery_app.autodiscover_tasks(["app.celery"])


if __name__ == "__main__":
    celery_app.start()