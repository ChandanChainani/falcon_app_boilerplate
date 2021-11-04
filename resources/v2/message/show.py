class Show():

    def on_get(self, req, res, message_id):
        """Handles GET requests"""
        data = {
            "message": f"message show v2 for {message_id}"
        }

        res.media = data
