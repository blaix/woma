from unittest import TestCase

from woma.http import Client

from examples.helloworld.app import router


class TestHelloWorldExample(TestCase):
    client = Client(router)

    def test_404s_for_unknown_path(self):
        response = self.client.get('/asdf')
        self.assertEqual(response.status_code, 404)

    def test_200s_for_matched_paths(self):
        response = self.client.get('/hello/asdf')
        self.assertEqual(response.status_code, 200)

    def test_says_hello_to_name(self):
        hello_bob_response = self.client.get('/hello/Bob')
        hello_amy_response = self.client.get('/hello/Amy')

        self.assertEqual(hello_bob_response.body, b'Hello Bob!\n')
        self.assertEqual(hello_amy_response.body, b'Hello Amy!\n')

    def test_says_goodbye_to_name(self):
        goodbye_bob_response = self.client.get('/goodbye/Bob')
        goodbye_amy_response = self.client.get('/goodbye/Amy')

        self.assertEqual(goodbye_bob_response.body, b'Goodbye Bob!\n')
        self.assertEqual(goodbye_amy_response.body, b'Goodbye Amy!\n')
