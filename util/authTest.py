import unittest
from unittest.mock import MagicMock
from auth import *
from request import Request


class MyTestCase(unittest.TestCase):

    def test_login(self):
        request = Request(b'POST /login HTTP/1.1\r\nHost: localhost:8080\r\nConnection: '
                          b'keep-alive\r\n\r\nusername=dominic&password=pennacchio')
        self.assertEqual(["dominic","pennacchio"], extract_credentials(request))  # add assertion here

    def test_register(self):
        request = Request(b'POST /register HTTP/1.1\r\nHost: localhost:8080\r\nConnection: '
                          b'keep-alive\r\n\r\nusername=dominic&password=pennacchio')
        self.assertEqual(["dominic","pennacchio"], extract_credentials(request))

    def test_passNum(self):
        request = Request(b'POST /login HTTP/1.1\r\nHost: localhost:8080\r\nConnection: '
                          b'keep-alive\r\n\r\nusername=nucherino&password=pennacchio1999')
        self.assertEqual(["nucherino","pennacchio1999"], extract_credentials(request))

    def test_passValidate1(self):
        password = "1qaz2wsx3EDC!)"
        self.assertEqual(True, validate_password(password))

    def test_passNoSpecChar(self):
        password = "1qaz2wsx3EDC3"
        self.assertEqual(False, validate_password(password))

    def test_passUnder8(self):
        password = "1QaZ!"
        self.assertEqual(False, validate_password(password))

    def test_passInvalidChar(self):
        password = "1Qaz@wsx3edc+"
        self.assertEqual(False, validate_password(password))

if __name__ == '__main__':
    unittest.main()
