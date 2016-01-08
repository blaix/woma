from unittest import TestCase
from unittest.mock import Mock

from woma.router import Router, Route
from woma.endpoints import not_found


class RouterTestCase(TestCase):
    def setUp(self):
        self.routes = Mock()
        self.router = Router(self.routes)


class TestRouterInit(RouterTestCase):
    """Router()"""

    def test_sets_default_route_to_not_found_handler(self):
        default = Route(path=None, endpoint=not_found)
        self.routes.setdefault.assert_called_once_with(default)


class TestRouterAdd(RouterTestCase):
    """router.add(path, endpoint)"""

    def test_adds_route_to_routes(self):
        path = '/path'
        endpoint = Mock()
        expected_route = Route(path=path, endpoint=endpoint)

        self.router.add(path, endpoint)

        self.routes.add.assert_called_once_with(expected_route)


class TestRouterSetDefault(RouterTestCase):
    """router.setdefault(endpoint)"""

    def test_sets_default_route_to_endpoint(self):
        endpoint = Mock()
        expected_route = Route(path=None, endpoint=endpoint)

        self.router.setdefault(endpoint)

        self.routes.setdefault.assert_called_with(expected_route)


class TestRouterCall(RouterTestCase):
    """router(environ, start_response)"""

    def setUp(self):
        super(TestRouterCall, self).setUp()
        self.environ = {'PATH_INFO': '/path'}
        self.start_response = Mock()
        self.response = self.router(self.environ, self.start_response)

    def test_gets_route_for_request_path(self):
        self.routes.get.assert_called_once_with('/path')

    def test_adds_router_kwargs_to_environ(self):
        route = self.routes.get.return_value
        self.assertEqual(self.environ['router.kwargs'], route.kwargs)

    def test_returns_call_to_routes_endpoint(self):
        route = self.routes.get.return_value
        route.endpoint.assert_called_once_with(
            self.environ, self.start_response)
        self.assertEqual(self.response, route.endpoint.return_value)
