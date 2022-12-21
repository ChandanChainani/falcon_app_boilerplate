class MessageById:

    def v2_after_validation(self, req, res):
        print("message v2 after_validation")

    def v2_get(self, req, res, **kwargs):
        """Handles GET requests"""
        data = {
            "message": "message v2 for %s" % kwargs['message_id']
        }

        res.media = data

