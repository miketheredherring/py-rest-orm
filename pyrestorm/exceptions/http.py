# HTTP Class Exceptions


class HttpException(Exception):
    pass


class ServerErrorException(HttpException):
    # HTTP 500
    pass


class MethodNotAllowedException(HttpException):
    # HTTP 405
    pass


class NotFoundException(HttpException):
    # HTTP 404
    pass


class PermissionDeniedException(HttpException):
    # HTTP 403
    pass


class AuthorizationException(HttpException):
    # HTTP 401
    pass


class BadRequestException(HttpException):
    # HTTP 400
    pass
