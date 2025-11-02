from celery.schedules import crontab
from app.celery.config import celery_app

#-- shudler -- : manage the periodic tasks,programte when execute tasks
celery_app.conf.beat_schedule = {
    'test-cada-minuto': {
        'task': 'tasks.prueba',
        'schedule': crontab(minute='*/1'),
    },
    "scraper-diario-0032": {
        "task": "app.utils.tasks.scrape_and_save_with_jitter",
        "schedule": crontab(minute=32, hour=0),
        "args": (180,),  # jitter máx 180s (3 min). Cambia a 0 si no quieres jitter.
    },
    "verificar-alertas-0800": {
        "task": "app.utils.tasks.verificar_alertas",
        "schedule": crontab(minute=0, hour=8),
    }
}

# shudler ->  broker -> worker -> task execute