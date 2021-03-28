import os
from datetime import datetime
from celery.app.base import Celery
from celery.schedules import crontab
from app.config import ApiAppConfig
from .cron_job import CRON_JOBS

celery = Celery('tasks')

default_config = dict(
    task_ignore_result=True,
    task_store_errors_even_if_ignored=True,
    timezone='Asia/Ho_Chi_Minh',
)

app_config_dict = {k: v for k, v in ApiAppConfig.__dict__.items() if not (k.startswith('__') and k.endswith('__'))}
default_config.update(app_config_dict)

# load config from local_config
try:
    from app import config_local

    config_local_dict = {k: v for k, v in config_local.__dict__.items()
                         if not (k.startswith('__') and k.endswith('__'))}
    default_config.update(config_local_dict)
except Exception as e:
    print("No config for local machine")

default_config.pop('os', "")
celery.conf.update(default_config)

# increase timeout following longest task in celery countdown
celery.conf.broker_transport_options = {'visibility_timeout': 8 * 86400}

# celery beat schedule use default UTC timezone
today = datetime.utcnow()
celery.conf.beat_schedule = CRON_JOBS
print("CELERY APP start success at {}".format(str(today)))
