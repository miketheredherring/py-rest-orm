import mock
from unittest import TestCase

from pyrestorm.client import RestClient
from pyrestorm import exceptions


class RestClientTestCase(TestCase):
    def test_request_valid_method(self):
        client = RestClient()
        response = client.request('GET', 'http://jsonplaceholder.typicode.com/posts/1')
        self.assertEqual(response['id'], 1)

    def test_request_invalid_method(self):
        client = RestClient()
        self.assertRaises(ValueError, client.request, 'INVALID', 'http://www.google.com/')

    def test_raises_exception(self):
        exs = (
            (500, exceptions.http.ServerErrorException),
            (405, exceptions.http.MethodNotAllowedException),
            (404, exceptions.http.NotFoundException),
            (403, exceptions.http.PermissionDeniedException),
            (401, exceptions.http.AuthorizationException),
            (400, exceptions.http.BadRequestException),
        )

        class MockResponse(object):
            def __init__(self, status_code):
                self.status_code = status_code
                self.content = ''

        client = RestClient()
        for code, ex in exs:
            response = MockResponse(code)
            self.assertRaises(ex, client.raise_exception, response)

    def test_get(self):
        client = RestClient()
        response = client.get('http://jsonplaceholder.typicode.com/posts/1')
        self.assertEqual(response['id'], 1)

    def test_post(self):
        client = RestClient()
        obj = {
            'title': 'The Great Gatsby',
            'body': 'In the end we are all humans, just...',
            'userId': 1
        }
        response = client.post('http://jsonplaceholder.typicode.com/posts', obj)
        self.assertEqual(client._response.status_code, 201)
        self.assertEqual(response['id'], 101)
        self.assertEqual(response['title'], obj['title'])

    def test_put(self):
        client = RestClient()
        obj = {
            'title': 'The Great Gatsby',
            'body': 'In the end we are all humans, just...',
            'userId': 2
        }
        response = client.put('http://jsonplaceholder.typicode.com/posts/1', obj)
        self.assertEqual(client._response.status_code, 200)
        self.assertEqual(response['userId'], 2)
        self.assertEqual(response['title'], obj['title'])

    def test_patch(self):
        client = RestClient()
        obj = {
            'body': 'In the end we are all humans, just...',
        }
        response = client.patch('http://jsonplaceholder.typicode.com/posts/1', obj)
        self.assertEqual(client._response.status_code, 200)
        self.assertEqual(response['id'], 1)
        self.assertEqual(response['body'], obj['body'])
        self.assertEqual(response['userId'], 1)

    def test_delete(self):
        client = RestClient()
        client.delete('http://jsonplaceholder.typicode.com/posts/1')
        self.assertEqual(client._response.status_code, 200)
