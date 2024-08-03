import re


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, func):
        self.routes[(method, path)] = func
        return

    def route_request(self, request):
        path = request.path
        method = request.method
        for (methodGot, pathGot), func in self.routes.items():
            pattern = pathGot
            if re.match(pattern, path) and methodGot == method:
                return func(request)
        text1 = ("HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/plain\r\n"
                 "X-Content-Type-Options: nosniff\r\nContent-Length: 36"
                 "\r\n\r\nThe requested content does not exist")
        fulltext = text1.encode()
        return fulltext
