import requests
from nprestclient.base import RestException


_METHODS = {
            'get' : requests.get,
            'put' : requests.put,
            'post' : requests.post,
            'delete' : requests.delete
            }


class ResponseGetter(object):
    def __init__(self, method, url, headers, data):
        method = method.lower()
        assert method in _METHODS, "Unknown method %s" % method
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        

    def get(self):
        resp = _METHODS[self.method](self.url, headers = self.headers, data = self.data)
        if resp.status_code >= 400:
            raise RestException(self.method,
                                self.url,
                                resp.status_code,
                                resp.text)
        try:
            return resp.json()
        except ValueError:
            return resp.text


class RequestsClient(object):
    def start_req(self, method, prepared_url, headers, body = ''):
        return ResponseGetter(method, prepared_url, headers, body)

    def wait_all_requests_completed(self):
        pass
