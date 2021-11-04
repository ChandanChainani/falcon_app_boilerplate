class MessageV2:

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message v2"
        }

        res.media = data
