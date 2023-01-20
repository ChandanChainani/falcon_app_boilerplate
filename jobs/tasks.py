from time import sleep
from datetime import datetime

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def sleep_for(seconds=30):
    sleep(seconds)
    return "OK"

@shared_task
def test():
    logger.info("Running `test` at %s" % datetime.now())
    return "Done"

