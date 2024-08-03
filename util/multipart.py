class MultipartData:
    def __init__(self, boundary, parts):
        self.boundary = boundary
        self.parts = parts

class MultipartPart:
    def __init__(self, headers, name, content_type, content):
        self.headers = headers
        self.name = name
        self.content_type = content_type
        self.content = content
        print(self.content)

def parse_multipart(request):
    boundary = request.headers["Content-Type"].split("=", 1)[1]
    parts = []
    bodySplits = request.body.split(b'\r\n--' + boundary.encode())
    for body in bodySplits:
        print(body)
        if len(body) < 3:  # Skip empty or boundary-only parts
            continue
        insideSplit = body.split(b'\r\n\r\n', 1)
        if len(insideSplit) < 2:  # Skip parts without headers or content
            continue
        headers_str = insideSplit[0].decode()
        content = insideSplit[1]
        headers = {}
        name = ""
        content_type = ""
        for header in headers_str.split('\r\n')[1:]:
            print("Header: ")
            print(header)
            head, value = header.split(':', 1)
            head = head.strip()
            value = value.strip()
            headers[head] = value
            if head.lower() == "content-type":
                content_type = value
                print("Content Type: ")
                print(content_type)
        disposition = headers["Content-Disposition"]
        dispositionParts = disposition.split("; ")
        for part in dispositionParts:
            part = part.strip()
            if part.startswith("name="):
                name = part.split("=")[1].strip('"')
                print("Name: ")
                print(name)
        print("Content: ")
        print(content)
        parts.append(MultipartPart(headers, name, content_type, content))
    return MultipartData(boundary, parts)
