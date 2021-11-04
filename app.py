import falcon

from resources.v1.message.index import MessageV1
from resources.v2.message.index import MessageV2

app = falcon.App()

app.add_route('/api/v1/message', MessageV1())
app.add_route('/api/v2/message', MessageV2())
