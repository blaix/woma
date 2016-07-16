from unittest import TestCase

from woma.endpoints import Endpoint


class TestEndpointEquality(TestCase):
    def test_equal_if_controllers_are_equal(self):
        controller1, controller2 = object(), object()
        endpoint1 = Endpoint(get=controller1, post=controller2)
        endpoint2 = Endpoint(get=controller1, post=controller2)
        self.assertEqual(endpoint1, endpoint2)

    def test_not_equal_if_controllers_differ(self):
        controller1, controller2 = object(), object()
        endpoint1 = Endpoint(get=controller1, post=controller2)
        endpoint2 = Endpoint(get=controller1, delete=controller2)
        self.assertNotEqual(endpoint1, endpoint2)
