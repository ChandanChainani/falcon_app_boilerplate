class Message:

    def v1_before_validation(self, req, res):
        print("message v1 before_validation")

    def v1_get(self, req, res, **kwargs):
        """Handles GET requests"""
        data = {
            "message": "message v1"
        }

        res.media = data

    def v2_after_validation(self, req, res):
        print("message v2 after_validation")

    def v2_get_by_id(self, req, res, **kwargs):
        """Handles GET requests"""
        data = {
            "message": "message v2 for %s" % kwargs['message_id']
        }

        res.media = data

