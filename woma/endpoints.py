from woma.controllers import not_found
from woma.http import Request, Response


class Endpoint(object):
    """A WSGI app that maps requests to controllers.

    For example:

    >>> from woma.http import Client
    >>> my_controller = lambda request, response: response
    >>> my_endpoint = Endpoint(my_controller)
    >>> Client(my_endpoint).get().status_code
    200

    """
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response.for_request(request)

        response = self.controller(request, response)
        return response(environ, start_response)


not_found = Endpoint(not_found)
