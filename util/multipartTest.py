import unittest
from request import Request
from multipart import *
class TestMultipartParsing(unittest.TestCase):
    def test_parse_multipart(self):
        requestBytes = (b'POST /form-path HTTP/1.1\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; '
                b'boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\n'
                b'Content-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n'
                b'------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: '
                b'form-data; name="upload"; filename="discord.png"\r\nContent-Type: '
                b'image/png\r\n\r\n<bytes_of_the_file>\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia--')

        requestObj = Request(requestBytes)
        multipartParsed = parse_multipart(requestObj)

        self.assertEqual(multipartParsed.boundary, "----WebKitFormBoundarycriD3u6M0UuPR1ia")
        part0 = MultipartPart({'Content-Disposition': 'form-data; name="commenter"'}, 'commenter', '', b'Jesse')
        self.assertEqual(multipartParsed.parts[0].headers, part0.headers)
        self.assertEqual(multipartParsed.parts[0].content_type, part0.content_type)
        self.assertEqual(multipartParsed.parts[0].name, part0.name)
        self.assertEqual(multipartParsed.parts[0].content, part0.content)

if __name__ == "__main__":
    unittest.main()
