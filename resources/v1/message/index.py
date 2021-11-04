class Index:

    def before_validation(self, req, res):
        print("message v1 before_validation")

    def on_get(self, req, res):
        """Handles GET requests"""
        data = {
            "message": "message v1"
        }

        res.media = data

resource_instance = Index()
