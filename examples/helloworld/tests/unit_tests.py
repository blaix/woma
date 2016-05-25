from unittest import TestCase

from tdubs import calling, verify, Mock, Stub

from examples.helloworld.app import say_hello, say_goodbye, GreetingController


class TestSayHello(TestCase):
    def test_says_hello_to_name(self):
        result = say_hello('Justin')
        self.assertEqual(result, 'Hello Justin!\n')


class TestSayGoodbye(TestCase):
    def test_says_goodbye_to_name(self):
        result = say_goodbye('Mary')
        self.assertEqual(result, 'Goodbye Mary!\n')


class TestGreetingController(TestCase):
    def setUp(self):
        greeter = Stub('greeter')
        calling(greeter).passing('the name').returns('the greeting')

        self.controller = GreetingController(greeter)
        self.request = Stub('request', kwargs={'name': 'the name'})
        self.response = Mock('response')

    def test_sets_greeter_result_as_response_text(self):
        response = self.controller(self.request, self.response)
        verify(response.write).called_with('the greeting')
