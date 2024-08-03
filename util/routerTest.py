import unittest
from unittest.mock import MagicMock
from router import Router
from request import Request


class TestRouter(unittest.TestCase):

    def test_add_route(self):
        router = Router()
        method = 'GET'
        path = '/test'
        func = MagicMock()
        router.add_route(method, path, func)

        self.assertEqual(router.routes[(method, path)], func)

    def test_route_request_found(self):
        router = Router()
        method = 'GET'
        path = '/test'
        func = MagicMock(return_value=b'Test response')
        request = Request(b'GET /test HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
        router.add_route(method, path, func)

        response = router.route_request(request)
        self.assertEqual(response, b'Test response')

    def test_route_request_not_found(self):
        router = Router()
        method = 'GET'
        path = '/unknown'
        request = Request(b'GET /unknown HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')

        response = router.route_request(request)
        expected_response = (b"HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/plain\r\nX-Content-Type-Options: "
                             b"nosniff\r\nContent-Length: 36\r\n\r\nThe requested content does not exist")
        self.assertEqual(response, expected_response)

    def test_route_request_method(self):
        router = Router()
        method_post = 'POST'
        path_post = '/test'
        func_post = MagicMock(return_value=b'Test response for POST')
        request_post = Request(b'POST /test HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
        router.add_route(method_post, path_post, func_post)

        response_post = router.route_request(request_post)
        self.assertEqual(response_post, b'Test response for POST')

    def test_multiple_route_request_method(self):
        router = Router()
        method_get = 'GET'
        path_get = '/test'
        func_get = MagicMock(return_value=b'Test response for GET')
        request_get = Request(b'GET /test HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
        router.add_route(method_get, path_get, func_get)

        method_post = 'POST'
        path_post = '/test'
        func_post = MagicMock(return_value=b'Test response for POST')
        request_post = Request(b'POST /test HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
        router.add_route(method_post, path_post, func_post)

        response_get = router.route_request(request_get)
        self.assertEqual(response_get, b'Test response for GET')
        response_post = router.route_request(request_post)
        self.assertEqual(response_post, b'Test response for POST')


if __name__ == '__main__':
    unittest.main()
