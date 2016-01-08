"""HTTP Request and Response objects.

These are the objects that are passed to controllers.

They inherit from webob's Request and Response objects, so see
http://docs.webob.org/en/latest/ for full documentation. The only things
documented here are the customizations.

"""
from webob import Request as BaseRequest
from webob import Response as BaseResponse


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
