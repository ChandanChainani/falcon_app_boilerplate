class Index:

    def after_validation(self, req, res):
        print("message v2 after_validation")

    def on_get(self, req, res, message_id):
        """Handles GET requests"""
        data = {
            "message": f"message v2 for {message_id}"
        }

        res.media = data

resource_instance = Index()
