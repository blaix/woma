import re

from property_caching import cached_property
from webob import Request

from woma.endpoints import Endpoint, not_found
from woma.exceptions import NotFound


class Router(object):
    """Map URL paths to handlers. Supports being used as WSGI callable.

    High-level API
    ---------------

        from woma.router import Router
        router = Router()

    You will usually route paths to controllers:

        router.add('/path', get=my_controller, post=my_other_controller)

    All of the HTTP verbs are supported as kwargs.

    Dynamic path segments
    ----------------------

    Your path can contain dynamic sections:

        router.add('/articles/{article_id}', get=get_article, post=add_article)

    When the controller is called, the passed ``request`` object will have a
    ``kwargs`` property that holds a dict of the values passed in the dynamic
    parts of the URL. For example, on requests to ``/articles/3``,
    the incoming ``request.kwargs`` will be ``{'article_id': 3}``.

    Low-level API
    --------------

    Interally, controllers are wrapped in a `woma.endpoints.Endpoint`.  If you
    need to customize the endpoint (e.g. to add middleware), you can route
    paths directly to endpoints yourself. The above example is equivalent to:

        article_endpoint = Endpoint(get=get_article, post=add_article)
        router.map_endpoint('/articles/{article_id}', endpoint)

    If you need to get even lower-level, you can define `woma.router.Route`
    objects yourself. The above example is equivalent to:

        article_endpoint = Endpoint(get=get_article, post=add_article)
        route = Route('/articles/{article_id}', endpoint)
        router.add_route(route)

    **WSGI:**

    Routers are WSGI callables. See `woma.router.Route.__call__` for details.

    """

    def __init__(self, routes=None):
        """Initialize a router, optionally with a preloaded Routes object.

        It sets the default endpoint to woma.endpoints.not_found.

        """
        self.routes = routes or Routes()
        self.setdefault(not_found)

    @property
    def add(self):
        """router.add is an alias for router.map_controllers"""
        return self.map_controllers

    def add_route(self, route):
        """Add a predefined route to the router.

        For example:

            route = Route('/path', endpoint)
            router.add_route(route)

        This is a low-level method. Usually, you don't need to define route
        objects yourself, and can use .add, .map_controllers, or .map_endpoint
        instead. See the documentation for those methods.

        """
        self.routes.add(route)

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
        self.add_route(route)

    def map_controllers(self, path, default_controller=None, **controllers):
        """Create an endpoint for the given controllers and add it to router.

        Example:

            router.map_controllers('/path', get=controller1, post=controller2)

        is equivalent to:

            endpoint = Endpoint(get=controller1, post=controller2)
            router.map_endpoint('/path', endpoint)

        See docs for Router.map_endpoint for more details.

        """
        endpoint = Endpoint(default_controller, **controllers)
        self.map_endpoint(path, endpoint)

    def setdefault(self, endpoint):
        """Set the default endpoint to use for unmatched paths."""
        route = Route(path=None, endpoint=endpoint)
        self.routes.setdefault(route)

    def __call__(self, environ, start_response):
        """The wsgi callable.

        When called, a route is found that matches the path in the ``environ``,
        and ``environ`` and ``start_response`` are passed through to the
        route's ``endpoint`` property, and the result is returned.

        Dynamic path segments are added as a ``'router.kwargs'`` key to the
        ``environ`` before passing it to the endpoint. The endpoint is the
        thing that turns that into ``request.kwargs`` when calling controllers.

        """
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
