from unittest import TestCase

from woma.http import Request


class TestRequest(TestCase):
    def test_kwargs_default_to_empty_dict(self):
        request = Request({})
        self.assertEqual(request.kwargs, {})

    def test_kwargs_returns_router_kwargs_from_environ(self):
        request = Request({'router.kwargs': {'foo': 'bar'}})
        self.assertEqual(request.kwargs, {'foo': 'bar'})
