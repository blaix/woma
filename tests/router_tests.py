from unittest import TestCase

from tdubs import calling, verify, Mock, Stub

from woma.router import Router, Route
from woma.endpoints import Endpoint, not_found


class RouterTestCase(TestCase):
    def setUp(self):
        self.routes = Mock('routes')
        self.router = Router(self.routes)


class TestRouterInit(RouterTestCase):
    """Router()"""

    def test_sets_default_route_to_not_found_handler(self):
        default = Route(path=None, endpoint=not_found)
        verify(self.routes.setdefault).called_with(default)


class TestRouterMapEndpoint(RouterTestCase):
    """router.map_endpoint(path, endpoint)"""

    def test_adds_route_to_routes(self):
        endpoint = Stub('endpoint')
        expected_route = Route(path='/path', endpoint=endpoint)
        self.router.map_endpoint('/path', endpoint)
        verify(self.routes.add).called_with(expected_route)


class TestRouterMapControllers(RouterTestCase):
    """router.map_controllers(path, **controllers)"""

    @property
    def subject(self):
        # The subject of this test, abstracted to test shared behavior
        return self.router.map_controllers

    def test_adds_an_endpoint_to_router_for_the_given_controllers(self):
        controller1, controller2 = object(), object()
        expected_endpoint = Endpoint(get=controller1, post=controller2)
        expected_route = Route(path='/path', endpoint=expected_endpoint)
        self.subject('/path', get=controller1, post=controller2)
        verify(self.routes.add).called_with(expected_route)

    def test_accepts_default_controller(self):
        """can also be called like: router.map_controllers(path, controller)"""
        controller = object()
        expected_endpoint = Endpoint(controller)
        expected_route = Route('/the/path', endpoint=expected_endpoint)
        self.subject('/the/path', controller)
        verify(self.routes.add).called_with(expected_route)


class TestRouterMap(TestRouterMapControllers):
    """router.map aliases router.map_controllers"""

    @property
    def subject(self):
        # The subject of this test, abstracted to test shared behavior
        return self.router.map


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
