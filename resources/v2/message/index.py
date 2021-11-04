class Index:

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message v2"
        }

        res.media = data

resource_instance = Index()
