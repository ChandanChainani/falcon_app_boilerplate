import falcon

from custom.routers.version import Version as VersionRouter
from custom.middlewares.logging import Logging
from custom.middlewares.validation import Validation
from resources.message import Message
from resources.message_by_id import MessageById

MIDDLEWARES = [
    Logging(),
    Validation(),
]

version_router = VersionRouter()
app = falcon.App(router=version_router, middleware=MIDDLEWARES)
app.add_route('/{version}/message', Message())
app.add_route('/{version}/message/{message_id}', MessageById())

