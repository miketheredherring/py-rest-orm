class ServerErrorException(Exception):
    # HTTP 500
    pass


class NotFoundException(Exception):
    # HTTP 404
    pass


class PermissionDeniedException(Exception):
    # HTTP 403
    pass


class AuthenticationException(Exception):
    # HTTP 401
    pass


class BadRequestException(Exception):
    # HTTP 400
    pass
