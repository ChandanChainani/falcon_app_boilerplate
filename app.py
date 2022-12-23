import falcon

from custom.routers.version import Version as VersionRouter
from custom.middlewares.logging import Logging
from custom.middlewares.validation import Validation
from resources.message import Message

MIDDLEWARES = [
    Logging(),
    Validation(),
]

version_router = VersionRouter()
app = falcon.App(router=version_router, middleware=MIDDLEWARES)
message = Message()
app.add_route('/{version}/message', message)
app.add_route('/{version}/message/{message_id}', message, options={
    "suffix": "by_id"
})

