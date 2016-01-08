from unittest import TestCase

from woma.http import Request, Response


class TestResponseForRequest(TestCase):
    """Response.for_request(request)"""

    def setUp(self):
        self.request = Request({})

    def test_sets_default_status_to_200(self):
        response = Response.for_request(self.request)
        self.assertEqual(response.status_code, 200)

    def test_sets_default_content_type_to_plain_text(self):
        response = Response.for_request(self.request)
        self.assertEqual(response.content_type, 'text/plain')

    def test_uses_content_type_of_request_if_present(self):
        self.request.content_type = 'application/json'
        response = Response.for_request(self.request)
        self.assertEqual(response.content_type, 'application/json')

    def test_sets_default_charset_to_utf8(self):
        response = Response.for_request(self.request)
        self.assertEqual(response.charset, 'UTF-8')

    def test_uses_charset_of_request_if_present(self):
        self.request.headers['Content-Type'] = 'text/plain; charset=ascii'
        response = Response.for_request(self.request)
        self.assertEqual(response.charset, 'ascii')
