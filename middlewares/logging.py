class Logging():
    def process_request(self, req, res):
        print("Logging: Process the request before routing it.")

    def process_resource(self, req, res, resource, params):
        print("Logging: Process the request after routing.")

    def process_response(self, req, res, resource, req_succeeded):
        print("Logging: Post-processing of the response (after routing).")
