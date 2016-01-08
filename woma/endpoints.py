from woma.controllers import not_found
from woma.http import Request, Response


class Endpoint(object):
    """Wrap a controller in an Endpoint to turn it into a full wsgi app.

    >>> my_controller = lambda request, response: response
    >>> my_endpoint = Endpoint(my_controller)

    >>> request = Request.blank('/')
    >>> status, headers, body = request.call_application(my_endpoint)
    >>> status
    '200 OK'

    """
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response.for_request(request)

        response = self.controller(request, response)
        return response(environ, start_response)


not_found = Endpoint(not_found)
