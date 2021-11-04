import falcon

class MessageV1:

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message v1"
        }

        res.media = data

class MessageV2:

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message v2"
        }

        res.media = data


app = falcon.App()
app.add_route('/api/v1/message', MessageV1())
app.add_route('/api/v2/message', MessageV2())
