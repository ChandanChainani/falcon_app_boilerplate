class MessageV1:

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message v1"
        }

        res.media = data
