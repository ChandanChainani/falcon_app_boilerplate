beat_schedule = {
    'add-every-30-seconds': {
        'task': 'jobs.tasks.test',
        'schedule': 30.0,
        'args': ()
    },
}

timezone = 'UTC'
