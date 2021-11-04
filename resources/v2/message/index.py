class Index():

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message index v2"
        }

        res.media = data
