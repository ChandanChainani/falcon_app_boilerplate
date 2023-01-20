from celery.result import AsyncResult

from jobs.tasks import sleep_for

class Job:

    def v1_get_by_task_id(self, req, res, **kwargs):
        """Handles Get JOB Status requests"""
        task = AsyncResult(kwargs['task_id'])
        res.media = {
            "state": task.state
        }

    def v1_post(self, req, res, **kwargs):
        """Handles Start JOB requests"""
        task = sleep_for.delay()
        res.media = {
            "task_id": task.task_id
        }

