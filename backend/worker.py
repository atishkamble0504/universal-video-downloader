from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0"
)