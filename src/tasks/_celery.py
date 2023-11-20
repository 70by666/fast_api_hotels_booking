from celery import Celery

from src.config import settings

celery = Celery(
    'tasks',
    broker=settings.REDIS,
    include=['src.tasks.tasks']
)
