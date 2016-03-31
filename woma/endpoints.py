from woma.controllers import not_found, method_not_allowed
from woma.http import Request, Response


class Endpoint(object):
    """The handler for a specific URL.

    It is a WSGI app that maps requests to controllers. A controller is any
    callable that accepts a request and response and returns a response.

    For example:

    >>> from woma.http import Client
    >>> my_controller = lambda request, response: response
    >>> my_endpoint = Endpoint(my_controller)
    >>> Client(my_endpoint).get().status_code
    200

    You can map different HTTP methods to different controllers. For example:

    >>> DB = []
    >>> def create_widget(request, response):
    ...     DB.append(request.text)
    ...     return response
    ...
    >>> def list_widgets(request, response):
    ...     response.text = ' '.join(DB)
    ...     return response
    ...
    >>> widget_collection = Endpoint(get=list_widgets, post=create_widget)
    >>> client = Client(widget_collection)
    >>> client.post(body='widget 1')
    <Response at ... 200 OK>
    >>> client.post(body='widget 2')
    <Response at ... 200 OK>
    >>> client.get().text
    'widget 1 widget 2'
    >>> client.put()
    <Response at ... 405 Method Not Allowed>

    You can put an endpoint behind a router to serve a particular URL:

    >>> from woma.router import Router
    >>> router = Router()
    >>> router.add('/widgets', widget_collection)
    >>> Client(router).get('/widgets').text
    'widget 1 widget 2'

    """
    def __init__(self, default=None, get=None, post=None, put=None, patch=None,
                 delete=None, head=None):
        default = default or method_not_allowed
        self.controllers = {
            'get': get or default,
            'post': post or default,
            'put': put or default,
            'patch': patch or default,
            'delete': delete or default,
            'head': head or default,
        }

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response.for_request(request)

        controller = self.controllers.get(
            request.method.lower(), method_not_allowed)
        response = controller(request, response)
        return response(environ, start_response)


not_found = Endpoint(not_found)
