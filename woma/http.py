"""Woma objects for dealing with HTTP.

Request and Response inherit from webob's Request and Response objects, so see
http://docs.webob.org/en/latest/ for full documentation. The only things
documented here are the customizations.

"""
from webob import Request as BaseRequest
from webob import Response as BaseResponse


class Client(object):
    """Make requests to a wsgi app and return the response."""

    def __init__(self, app):
        self.app = app

    def request(self, path, method):
        path = path or '/'
        request = BaseRequest.blank(path)
        request.method = method
        return request.get_response(self.app)

    def get(self, path=None):
        return self.request(path, 'GET')


class Request(BaseRequest):
    """A webob.Request with additional properties."""

    @property
    def kwargs(self):
        """Returns 'router.kwargs' from environ if present, or {} otherwise."""
        return self.environ.get('router.kwargs', {})


class Response(BaseResponse):
    """A webob.Response that can be initialized with defaults from request."""

    @classmethod
    def for_request(cls, request):
        """Initialize a Response with defaults based on the request.

        >>> request = Request({})
        >>> request.headers['Content-Type'] = 'text/html; charset=latin1'

        >>> response = Response.for_request(request)
        >>> response.content_type
        'text/html'
        >>> response.charset
        'latin1'

        """
        return cls(
            status_code=200,
            content_type=request.content_type or 'text/plain',
            charset=request.charset or 'UTF-8')
