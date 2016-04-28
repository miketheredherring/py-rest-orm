class RestFailure(Exception):
    # Base class for an operation not succeeding
    pass


class DoesNotExist(RestFailure):
    # Object matching GET query does not exist
    pass


class MultipleObjectsReturned(RestFailure):
    # Multiple objects matched GET query
    pass
