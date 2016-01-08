from unittest import TestCase

from woma.router import Route


class TestRoute(TestCase):
    def test_equals_another_route_only_if_paths_and_endpoints_match(self):
        route1 = Route('/foo', 'foo')
        route2 = Route('/foo', 'foo')

        route3 = Route('/foo', 'bar')
        route4 = Route('/bar', 'foo')

        self.assertEqual(route1, route2)
        self.assertNotEqual(route1, route3)
        self.assertNotEqual(route1, route4)


class TestRouteMatch(TestCase):
    """route.match(path)"""

    def test_returns_false_if_path_does_not_match_route_path(self):
        route = Route('/foo', 'foo')
        self.assertFalse(route.match('/bar'))

    def test_returns_true_if_path_matches_route_path(self):
        route = Route('/foo', 'foo')
        self.assertTrue(route.match('/foo'))

    def test_matches_keyword_arguments(self):
        route = Route('/{foo}/{bar}', 'foobar')
        self.assertTrue(route.match('/fizz/buzz'))

    def test_kwargs_are_added_to_matched_route(self):
        route = Route('/{one}/{two}', 'foo')
        route.match('/1/2')
        self.assertEqual(route.kwargs, {'one': '1', 'two': '2'})
