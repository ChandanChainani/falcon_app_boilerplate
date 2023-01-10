class Validation():
    def process_resource(self, req, res, resource, params):
        validate = getattr(resource, req.context.get('method_name', '') + '_before_validation', None)
        if validate:
            print("Validation: Before processing request")
            validate(req, res)

    def process_response(self, req, res, resource, req_succeeded):
        validate = getattr(resource, req.context.get('method_name', '') + '_after_validation', None)
        if validate:
            print("Validation: After response generation")
            validate(req, res)
