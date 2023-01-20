import falcon

from custom.routers.version import Version as VersionRouter
from custom.middlewares.logging import Logging
from custom.middlewares.validation import Validation
from resources.message import Message
from resources.job import Job

MIDDLEWARES = [
    Logging(),
    Validation(),
]

version_router = VersionRouter()
app = falcon.App(router=version_router, middleware=MIDDLEWARES)

class PingHandler():
    def on_get(self, req, res):
        res.text = "pong"
app.add_route('/ping', PingHandler())

message = Message()
app.add_route('/{version}/message', message)
app.add_route('/{version}/message/{message_id}', message, options={
    "suffix": "by_id"
})

job = Job()
app.add_route('/{version}/job', job)
app.add_route('/{version}/job/{task_id}', job, options={
    "suffix": "by_task_id"
})

