from .celery_app import celery
from . import background_task
from celery.signals import worker_ready


@worker_ready.connect
def at_start(sender, **k):
    celery.send_task('write_hello')
