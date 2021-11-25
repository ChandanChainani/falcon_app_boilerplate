class Validation():
    def process_resource(self, req, res, resource, params):
        req.context['_validator'] = '_validation' + "_" + params['version']
        validate = getattr(resource, "before" + req.context.get('_validator', ''), None)
        if validate:
            print("Validation: Before processing request")
            validate(req, res)

    def process_response(self, req, res, resource, req_succeeded):
        validate = getattr(resource, "after" + req.context.get('_validator', ''), None)
        if validate:
            print("Validation: After response generation")
            validate(req, res)
