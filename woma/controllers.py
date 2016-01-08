def not_found(request, response):
    """Basic controller to act as default for unmatched request paths."""
    response.status_code = 404
    response.text = "We can't find %s\n" % request.path
    return response
