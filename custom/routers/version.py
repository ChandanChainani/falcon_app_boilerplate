from falcon.routing import CompiledRouter

class Version(CompiledRouter):
    def find(self, uri, req=None):
        """Search for a route that matches the given partial URI.

        Args:
            uri(str): The requested path to route.

        Keyword Args:
            req: The :class:`falcon.Request` or :class:`falcon.asgi.Request`
                object that will be passed to the routed responder. Currently
                the value of this argument is ignored by
                :class:`~.CompiledRouter`. Routing is based solely on the path.

        Returns:
            tuple: A 4-member tuple composed of (resource, method_map,
            params, uri_template), or ``None`` if no route matches
            the requested path.
        """
        path = uri.lstrip('/').split('/')
        params = {}
        node = self._find(path, self._return_values, self._patterns,
                self._converters, params)

        if node is not None:
            method_name = req.method.lower() + "_" + params['version']
            _method = getattr(node.resource, method_name, None)
            if _method is None:
                return None
            node.method_map[req.method] = _method
            return node.resource, node.method_map, params, node.uri_template
        else:
            return None
