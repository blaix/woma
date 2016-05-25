def not_found(request, response):
    """Basic controller to act as default for unmatched request paths."""
    response.status_code = 404
    response.write("We can't find %s\n" % request.path)
    return response


def method_not_allowed(request, response):
    """Default controller used for requests for an unallowed HTTP method."""
    response.status_code = 405
    response.write('%s is not allowed\n' % request.method)
    return response
