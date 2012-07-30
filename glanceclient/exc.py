"""
Exception definitions.
"""


class CommandError(Exception):
    pass


class NoTokenLookupException(Exception):
    """This form of authentication does not support looking up
       endpoints from an existing token."""
    pass


class EndpointNotFound(Exception):
    """Could not find Service or Region in Service Catalog."""
    pass


class SchemaNotFound(KeyError):
    """Could not find schema"""
    pass


class InvalidEndpoint(ValueError):
    """The provided endpoint could not be used"""
    pass


class ClientException(Exception):
    """
    The base exception class for all exceptions this library raises.
    """
    def __init__(self, code, message=None, details=None):
        self.code = code
        self.message = message or self.__class__.message
        self.details = details

    def __str__(self):
        return "%s (HTTP %s)" % (self.message, self.code)


class BadRequest(ClientException):
    """
    HTTP 400 - Bad request: you sent some malformed data.
    """
    http_status = 400
    message = "Bad request"


class Unauthorized(ClientException):
    """
    HTTP 401 - Unauthorized: bad credentials.
    """
    http_status = 401
    message = "Unauthorized"


class Forbidden(ClientException):
    """
    HTTP 403 - Forbidden: your credentials don't give you access to this
    resource.
    """
    http_status = 403
    message = "Forbidden"


class NotFound(ClientException):
    """
    HTTP 404 - Not found
    """
    http_status = 404
    message = "Not found"


class Conflict(ClientException):
    """
    HTTP 409 - Conflict
    """
    http_status = 409
    message = "Conflict"


class OverLimit(ClientException):
    """
    HTTP 413 - Over limit: you're over the API limits for this time period.
    """
    http_status = 413
    message = "Over limit"


class InternalServerError(ClientException):
    """
    HTTP 500 - Internal Server Error
    """
    http_status = 500
    message = "Internal Server Error"


# NotImplemented is a python keyword.
class HTTPNotImplemented(ClientException):
    """
    HTTP 501 - Not Implemented: the server does not support this operation.
    """
    http_status = 501
    message = "Not Implemented"


class ServiceUnavailable(ClientException):
    """
    HTTP 503 - Service Unavailable
    """
    http_status = 503
    message = "Service Unavailable"


# In Python 2.4 Exception is old-style and thus doesn't have a __subclasses__()
# so we can do this:
#     _code_map = dict((c.http_status, c)
#                      for c in ClientException.__subclasses__())
#
# Instead, we have to hardcode it:
_exc_list = [BadRequest, Unauthorized, Forbidden, NotFound, OverLimit,
             InternalServerError, HTTPNotImplemented, ServiceUnavailable]
_code_map = dict((c.http_status, c) for c in _exc_list)


def from_response(response):
    """Return an instance of an ClientException based on httplib response."""
    cls = _code_map.get(response.status, ClientException)
    return cls(code=response.status)
