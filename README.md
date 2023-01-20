# falcon_app_boilerplate

- Pipenv for package/module management
- Gunicorn server for dev testing
  * cmd to start service: `pipenv run gunicorn app:app`
- Easy modularization and maintenance of code
- Custom version handler for routing request
  to version specific resource method
- Their can be specific version for resource at a time
  for eg. we can have version 1 for one resource and version 2
  for other resource
- Logging and Validation middleware is added for generic use cases
- Async Jobs using [`celery`](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) with scheduling support
  * cmd to start celery worker: `pipenv run celery worker -I $CELERY_IMPORTS -E -l INFO -B`
    + -B, --bea
      starts beat for scheduled job
    + -I, --include
      include tasks from module
    + -E, --task-events, --events
      Send task-related events that can be captured by monitors like celery events, celerymon, and others
    + -l, --loglevel <loglevel>
      Logging level
    + -f, --logfile <logfile>
      Location for file where celery log should be stored
    + -Q, --queue <queue>
      custom queue name
  * Environment variables for celery
    + CELERY_BROKER_URL=redis://localhost:6379/0
    + CELERY_RESULT_BACKEND=redis://localhost:6379/0
    + CELERY_CONFIG_MODULE=jobs.celeryconfig
    + CELERY_IMPORTS=jobs.tasks
