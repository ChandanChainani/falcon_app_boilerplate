class Index():

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message index v1"
        }

        res.media = data
