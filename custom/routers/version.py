from re import search as re_search

from falcon.routing import CompiledRouter
from falcon.routing.compiled import _FIELD_PATTERN, CompiledRouterNode
from falcon.routing.util import set_default_responders

class Version(CompiledRouter):
    def add_route(self, uri_template, resource, **kwargs):
        """Add a route between a URI path template and a resource.
        This method may be overridden to customize how a route is added.
        Args:
            uri_template (str): A URI template to use for the route
            resource (object): The resource instance to associate with
                the URI template.
        Keyword Args:
            suffix (str): Optional responder name suffix for this route. If
                a suffix is provided, Falcon will map GET requests to
                ``on_get_{suffix}()``, POST requests to ``on_post_{suffix}()``,
                etc. In this way, multiple closely-related routes can be
                mapped to the same resource. For example, a single resource
                class can use suffixed responders to distinguish requests
                for a single item vs. a collection of those same items.
                Another class might use a suffixed responder to handle
                a shortlink route in addition to the regular route for the
                resource.
            compile (bool): Optional flag that can be used to compile the
                routing logic on this call. By default, :class:`.CompiledRouter`
                delays compilation until the first request is routed. This may
                introduce a noticeable amount of latency when handling the first
                request, especially when the application implements a large
                number of routes. Setting `compile` to ``True`` when the last
                route is added ensures that the first request will not be
                delayed in this case (defaults to ``False``).
                Note:
                    Always setting this flag to ``True`` may slow down the
                    addition of new routes when hundreds of them are added at
                    once. It is advisable to only set this flag to ``True`` when
                    adding the final route.
        """

        # NOTE(kgriffs): falcon.asgi.App injects this private kwarg; it is
        #   only intended to be used internally.
        asgi = kwargs.get('_asgi', False)

        method_map = self.map_http_methods(resource, **kwargs)

        set_default_responders(method_map, asgi=asgi)

        if asgi:
            self._require_coroutine_responders(method_map)
        else:
            self._require_non_coroutine_responders(method_map)

        # NOTE(kgriffs): Fields may have whitespace in them, so sub
        # those before checking the rest of the URI template.
        if re_search(r'\s', _FIELD_PATTERN.sub('{FIELD}', uri_template)):
            raise UnacceptableRouteError('URI templates may not include whitespace.')

        path = uri_template.lstrip('/').split('/')

        used_names = set()
        for segment in path:
            self._validate_template_segment(segment, used_names)

        def find_cmp_converter(node):
            value = [
                (field, converter)
                for field, converter, _ in node.var_converter_map
                if converters._consumes_multiple_segments(
                    self._converter_map[converter]
                )
            ]
            if value:
                return value[0]
            else:
                return None

        def insert(nodes, path_index=0):
            for node in nodes:
                segment = path[path_index]
                if node.matches(segment):
                    path_index += 1
                    if path_index == len(path):
                        # NOTE(kgriffs): Override previous node
                        node.method_map = method_map
                        node.resource = resource
                        node.uri_template = uri_template
                        node.options = kwargs.get("options", None)
                    else:
                        cpc = find_cmp_converter(node)
                        if cpc:
                            raise UnacceptableRouteError(
                                _NO_CHILDREN_ERR.format(uri_template, *cpc)
                            )
                        insert(node.children, path_index)

                    return

                if node.conflicts_with(segment):
                    raise UnacceptableRouteError(
                        'The URI template for this route is inconsistent or conflicts '
                        "with another route's template. This is usually caused by "
                        'configuring a field converter differently for the same field '
                        'in two different routes, or by using different field names '
                        "at the same level in the path (e.g.,'/parents/{id}' and "
                        "'/parents/{parent_id}/children')"
                    )

            # NOTE(richardolsson): If we got this far, the node doesn't already
            # exist and needs to be created. This builds a new branch of the
            # routing tree recursively until it reaches the new node leaf.
            new_node = CompiledRouterNode(path[path_index])
            if new_node.is_complex:
                cpc = find_cmp_converter(new_node)
                if cpc:
                    raise UnacceptableRouteError(
                        'Cannot use converter "{1}" of variable "{0}" in a template '
                        'that includes other characters or variables.'.format(*cpc)
                    )
            nodes.append(new_node)
            if path_index == len(path) - 1:
                new_node.method_map = method_map
                new_node.resource = resource
                new_node.uri_template = uri_template
                new_node.options = kwargs.get("options", None)
            else:
                cpc = find_cmp_converter(new_node)
                if cpc:
                    # NOTE(caselit): assume success and remove the node if it's not
                    # supported to avoid leaving the router in a broken state.
                    nodes.remove(new_node)
                    raise UnacceptableRouteError(
                        _NO_CHILDREN_ERR.format(uri_template, *cpc)
                    )
                insert(new_node.children, path_index + 1)

        insert(self._roots)
        # NOTE(caselit): when compile is True run the actual compile step, otherwise
        # reset the _find, so that _compile will be called on the next find use
        if kwargs.get('compile', False):
            self._find = self._compile()
        else:
            self._find = self._compile_and_find

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
            method_name = "{}_{}".format(params['version'], req.method.lower())

            if node.options and node.options.get('suffix', None):
                method_name += "_" + node.options.get('suffix')
            _method = getattr(node.resource, method_name, None)
            if _method is None:
                return None
            node.method_map[req.method] = _method
            req.context['method_name'] = method_name
            req.context['version'] = params['version']
            return node.resource, node.method_map, params, node.uri_template
        else:
            return None
