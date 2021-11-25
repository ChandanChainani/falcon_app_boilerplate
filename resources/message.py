class Message:

    def before_validation_v1(self, req, res):
        print("message v1 before_validation")

    def get_v1(self, req, res, **kwargs):
        """Handles GET requests"""
        data = {
            "message": "message v1"
        }

        res.media = data

