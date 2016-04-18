from unittest import TestCase

from tdubs import calling, verify, Mock, Stub

from woma.router import Router, Route
from woma.endpoints import not_found


class RouterTestCase(TestCase):
    def setUp(self):
        self.routes = Mock('routes')
        self.router = Router(self.routes)


class TestRouterInit(RouterTestCase):
    """Router()"""

    def test_sets_default_route_to_not_found_handler(self):
        default = Route(path=None, endpoint=not_found)
        verify(self.routes.setdefault).called_with(default)


class TestRouterAdd(RouterTestCase):
    """router.add(path, endpoint)"""

    def test_adds_route_to_routes(self):
        endpoint = Stub('endpoint')
        expected_route = Route(path='/path', endpoint=endpoint)
        self.router.add('/path', endpoint)
        verify(self.routes.add).called_with(expected_route)


class TestRouterSetDefault(RouterTestCase):
    """router.setdefault(endpoint)"""

    def test_sets_default_route_to_endpoint(self):
        endpoint = Stub('endpoint')
        expected_route = Route(path=None, endpoint=endpoint)

        self.router.setdefault(endpoint)

        verify(self.routes.setdefault).called_with(expected_route)


class TestRouterCall(RouterTestCase):
    """router(environ, start_response)"""

    def setUp(self):
        super(TestRouterCall, self).setUp()

        self.environ = {'PATH_INFO': '/path'}
        start_response = Stub('start_response')

        route = Stub('route', kwargs={'expected': 'kwargs'})
        calling(route.endpoint).passing(self.environ, start_response).returns(
            'endpoint response')

        calling(self.routes.get).passing('/path').returns(route)

        self.response = self.router(self.environ, start_response)

    def test_adds_route_kwargs_to_environ(self):
        self.assertEqual(self.environ['router.kwargs'], {'expected': 'kwargs'})

    def test_returns_call_to_routes_endpoint(self):
        self.assertEqual(self.response, 'endpoint response')
