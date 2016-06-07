import json
import requests
import urllib

from exceptions.http import (
    ServerErrorException,
    NotFoundException,
    PermissionDeniedException,
    AuthorizationException,
    BadRequestException,
    MethodNotAllowedException
)
from utils import build_url


class StatusCodes(object):
    HTTP_OK = 200
    HTTP_CREATED = 201
    HTTP_NO_CONTENT = 204
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_PERMISSION_DENIED = 403
    HTTP_NOT_FOUND = 404
    HTTP_METHOD_NOT_ALLOWED = 405
    HTTP_SERVER_ERROR = 500


class RestClient(object):
    '''
    Generic client used for talking over HTTP, wrapper for requests with basic exeption handling.
    '''
    JSON = 'application/json'

    def __init__(self, token=None, authorization_header=None):
        self.headers = {}
        # If both of the settings are set, setup authorization
        if token is not None and authorization_header is not None:
            self.headers['Authorization'] = '%s %s' % (authorization_header, token)

    # Wrapper for requests library with response parsing and exception handler
    def request(self, method, url, *args, **kwargs):
        # Check for valid request method
        method = getattr(requests, method.lower(), method)

        # Programming error
        if isinstance(method, str):
            raise ValueError('Invalid method `%s` for requests' % method)

        # Add headers to the request
        kwargs['headers'] = self.headers

        # Perform the request
        self._response = method(url, *args, **kwargs)
        self.status_code = self._response.status_code

        # Handle exceptions
        self.raise_exception(self._response.status_code)

        # No exceptions means we should return the response
        return self.parse_response(self._response)

    # Codes which should not show up in a response for a valid request
    def raise_exception(self, status_code):
        if status_code == StatusCodes.HTTP_SERVER_ERROR:
            raise ServerErrorException
        elif status_code == StatusCodes.HTTP_METHOD_NOT_ALLOWED:
            raise MethodNotAllowedException
        elif status_code == StatusCodes.HTTP_NOT_FOUND:
            raise NotFoundException
        elif status_code == StatusCodes.HTTP_PERMISSION_DENIED:
            raise PermissionDeniedException
        elif status_code == StatusCodes.HTTP_UNAUTHORIZED:
            raise AuthorizationException
        elif status_code == StatusCodes.HTTP_BAD_REQUEST:
            raise BadRequestException

    # Takes the reponse and parses the correct content-type
    def parse_response(self, response):
        ret = response.content
        # JSON response
        if self.JSON in response.headers.get('content-type', 'plaintext'):
            ret = json.loads(response.content)

        return ret

    def get(self, url, *args, **kwargs):
        return self.request('GET', build_url(url, **kwargs))

    def post(self, url, data, *args, **kwargs):
        return self.request('POST', url, json=data)

    def patch(self, url, data, *args, **kwargs):
        return self.request('PATCH', url, json=data)

    def put(self, url, data, *args, **kwargs):
        return self.request('PUT', url, json=data)

    def delete(self, url, *args, **kwargs):
        return self.request('DELETE', url)
