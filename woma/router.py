import re

from property_caching import cached_property
from webob import Request

from woma.endpoints import not_found
from woma.exceptions import NotFound


class Router(object):
    """WSGI app that can route paths to other WSGI apps (called endpoints)."""

    def __init__(self, routes=None):
        """Initialize a router, optionally with a preloaded Routes object.

        It sets the default endpoint to woma.endpoints.not_found.

        """
        self.routes = routes or Routes()
        self.setdefault(not_found)

    def map_endpoint(self, path, endpoint):
        """Map the path to the given endpoint.

        - path: a string representing a URL path. e.g. '/articles'.
          It can contain dynamic segments of the form: '/articles/{article_id}'
          which will result in 'router.kwargs' being added to the environ
          with a dict holding the matched path segments.

        - endpoint: any valid wsgi app.
          e.g. an instance of woma.endpoints.Endpoint

        """
        route = Route(path, endpoint)
        self.routes.add(route)

    def setdefault(self, endpoint):
        """Set the default endpoint to use for unmatched paths."""
        route = Route(path=None, endpoint=endpoint)
        self.routes.setdefault(route)

    def __call__(self, environ, start_response):
        """The wsgi callable."""
        request = Request(environ)
        route = self.routes.get(request.path)
        environ['router.kwargs'] = route.kwargs
        return route.endpoint(environ, start_response)


class Routes(object):
    """A collection of Route objects."""

    def __init__(self):
        self.routes = []
        self.default = None

    def add(self, route):
        """Add a Route object to the collection."""
        self.routes.append(route)

    def get(self, path):
        """Return the Route object that matches the given path.

        If no match is found, the default will be returned, otherwise
        woma.exceptions.NotFound will be raised.

        """
        for route in self.routes:
            if route.match(path):
                return route
        return self._not_found(path)

    def setdefault(self, route):
        """Set default route to use when requesting a path with no match."""
        self.default = route

    def _not_found(self, path):
        if self.default:
            return self.default
        raise NotFound('No route found for %s' % path)


class Route(object):
    """An object representing a path to an endpoint.

    A path is a string representing the path part of a URL. An endpoint can be
    anything at this level. For example:

    >>> def my_app(): return 'Hello from my app!'
    >>> route = Route('/my/app', my_app)
    >>> route.match('/your/app')
    False
    >>> route.match('/my/app')
    True
    >>> route.endpoint()
    'Hello from my app!'

    Paths can contain dynamic segments:

    >>> route = Route('/articles/{article_id}', my_app)
    >>> route.match('/articles/123')
    True
    >>> route.kwargs
    {'article_id': '123'}

    """

    def __init__(self, path, endpoint):
        self.path = path
        self.endpoint = endpoint
        self.kwargs = {}

    def __eq__(self, other):
        return [self.path, self.endpoint] == [other.path, other.endpoint]

    def __repr__(self):
        return 'Route(path=%s)' % self.path

    @cached_property
    def _path_regex(self):
        # this is a very naive conversion of a path into a regex...
        pattern = self.path.replace('{', '(?P<').replace('}', '>[^/]+)')
        return re.compile(r'^%s$' % pattern)

    def match(self, path):
        """Return True if path matches the Route's path, False otherwise.

        If the route's path has dynamic segments (e.g. '/{foo}'), and the given
        path is a match, the matching segments will be made available as a dict
        at route.kwargs.

        """
        match = self._path_regex.match(path)
        if not match:
            return False

        self.kwargs = match.groupdict()
        return True
