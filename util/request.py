class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        self.body = b""
        self.method = ""  # POST, GET, PUT, DELETE, HEAD
        self.path = ""
        self.http_version = ""
        self.headers = {}
        self.cookies = {}

        requestStr = request  # First decode str
        requestList = requestStr.split(b'\r\n\r\n', 1)  # Split it on newline
        self.body = requestList[1]
        firstSplit = requestList[0].decode()
        firstSplitList = firstSplit.split("\r\n")  # Have to make sure spaces are there or else I split port
        secondSplitList = firstSplitList[0]
        secondSplitList2 = secondSplitList.split(" ")
        self.method = secondSplitList2[0]
        self.path = secondSplitList2[1]
        self.http_version = secondSplitList2[2]
        headerList = firstSplitList[1:]  # Debugger say last item in headList is " so I end one index early
        for header in headerList:  # Add headers to self.headers
            head, value = header.split(":", 1)
            head = head.strip()
            value = value.strip()
            self.headers[head] = value
        if "Cookie" in self.headers:  # If cookies were added to self.header add them to self.cookies
            fullStr = self.headers["Cookie"]
            splitStr = fullStr.split(";")
            for split in splitStr:
                cookie, value = split.split("=", 1)  # Cookie have different names and values so split it again
                cookie = cookie.strip()
                value = value.strip()
                self.cookies[cookie] = value  # Hope and pray these names are all unique



def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

def test2():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCookie: id=X6kAwpgW29M; visits=4\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    print(request.headers["Cookie"])
    assert request.headers["Cookie"] == "id=X6kAwpgW29M; visits=4"
    assert request.cookies["id"] == "X6kAwpgW29M"
    assert request.cookies["visits"] == "4"
if __name__ == '__main__':
    test1()
    test2()

# response = request.http_version + " 200 OK" + "\r\n"
# response =+ "Content-Type: image/jpeg" + "\r\n"
# response =+ "Content-Length: " + "\r\n"
# response =+ header
# response = response.encode("utf-8")
# response =+ img
