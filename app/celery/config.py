from celery import Celery
from app.core.config import settings

# Configuración de Celery para tareas de data analytics
celery_app = Celery(
    "dolar_analytics_tasks",
    broker=settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else "redis://localhost:6379/0",
    backend=settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else "redis://localhost:6379/0"
)

celery_app.conf.timezone = "America/Lima"
celery_app.conf.task_track_started = True
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.result_expires = 3600  # 1 hora

# Autodiscover tasks
celery_app.autodiscover_tasks(["app.celery"])

if __name__ == "__main__":
    celery_app.start()
