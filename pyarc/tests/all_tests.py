import unittest
from ..base import ClientBase


class TestClient(ClientBase):
    def just_get(self, path):
        return self.get(path)


class Test(unittest.TestCase):
    def test_https_no_verify(self):
        TestClient('https://example.com/').just_get('/')

    def test_https_verify(self):
        TestClient('https://example.com/',
                   verify = True).just_get('/')

    def test_async_https_no_verify(self):
        TestClient('https://example.com/',
                   async = True).just_get('/').get()

    def test_async_https_verify(self):
        TestClient('https://example.com/',
                   async = True,
                   verify = True).just_get('/').get()


if __name__ == '__main__':
    unittest.main()
