class Index:

    def after_validation(self, req, res):
        print("message v2 after_validation")

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message v2"
        }

        res.media = data

resource_instance = Index()
