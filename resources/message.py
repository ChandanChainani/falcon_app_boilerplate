class Message:

    def v1_before_validation(self, req, res):
        print("message v1 before_validation")

    def v1_get(self, req, res, **kwargs):
        """Handles GET requests"""
        data = {
            "message": "message v1"
        }

        res.media = data

