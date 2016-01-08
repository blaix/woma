from unittest import TestCase

from woma.exceptions import NotFound
from woma.router import Route, Routes


class TestRoutesGet(TestCase):
    """routes.get(path)"""

    def test_returns_route_that_matches_the_path(self):
        expected_foo_route = Route('/foo', 'foo')
        expected_bar_route = Route('/bar', 'bar')

        routes = Routes()
        routes.add(expected_foo_route)
        routes.add(expected_bar_route)

        foo_route = routes.get('/foo')
        bar_route = routes.get('/bar')

        self.assertEqual(foo_route, expected_foo_route)
        self.assertEqual(bar_route, expected_bar_route)

    def test_returns_default_route_if_no_path_matches(self):
        default = Route(path=None, endpoint='404 endpoint')
        routes = Routes()
        routes.setdefault(default)

        route = routes.get('/asdf')
        self.assertEqual(route, default)

    def test_raises_NotFound_if_no_matching_path_and_no_set_default(self):
        routes = Routes()
        with self.assertRaises(NotFound):
            routes.get('/asdf')
