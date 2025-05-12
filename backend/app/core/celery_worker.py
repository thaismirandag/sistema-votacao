from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "votos"},
}

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=30,
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
