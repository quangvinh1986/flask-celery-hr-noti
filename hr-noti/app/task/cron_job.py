from celery.schedules import crontab

CRON_JOBS = {
    'daily_health_check': {
        'task': 'daily_health_check',
        'schedule': crontab(day_of_week='mon-sun', minute=00),  # do action at 0 minute every hour
        'args': (),
    },
    'auto_check_hire_date': {
        'task': 'auto_check_hire_date',
        'schedule': crontab(day_of_week='mon-sun', hour=8, minute=00),
        'args': (),
    }
}
