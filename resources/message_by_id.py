class MessageById:

    def after_validation_v2(self, req, res):
        print("message v2 after_validation")

    def get_v2(self, req, res, **kwargs):
        """Handles GET requests"""
        data = {
            "message": "message v2 for %s" % kwargs['message_id']
        }

        res.media = data

