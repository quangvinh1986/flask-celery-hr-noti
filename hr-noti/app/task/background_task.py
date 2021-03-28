import logging
import os
from datetime import datetime
from .celery_app import celery
from .back_ground.common_task import CommonTask

logger = logging.getLogger(__name__)

common_task = CommonTask(celery.conf)


@celery.task(name='daily_health_check')
def daily_health_check():
    common_task.do_health_check()
    return "daily_health_check"


@celery.task(name='write_hello')
def write_hello():
    """
    write something to logs file for start
    """
    try:
        logger.info("Hello from celery task at {}. Ready for run!".format(str(datetime.now())))
    except Exception as ex:
        logger.error("write_hello task fail " + str(ex.__str__()))
