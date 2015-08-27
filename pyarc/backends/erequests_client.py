import logging
import erequests
from nprestclient.base import RestException


class ResultWrapper(object):
    def __init__(self, client, method, url):
        self.client = client
        self.method = method
        self.url = url
        self.response = None

    def get(self):
        if self.response is None:
            self.client.wait_all_requests_completed()
        if self.response.status_code >= 400:
            raise RestException(self.method,
                                self.url,
                                self.response.status_code,
                                self.response.text)
        try:
            return self.response.json()
        except ValueError:
            return self.response.text


_METHODS = {
            'get' : erequests.async.get,
            'put' : erequests.async.put,
            'post' : erequests.async.post,
            'delete' : erequests.async.delete
            }


class ERequestsClient(object):
    def __init__(self):
        self.requests_to_send = []
        self.results = []

    def start_req(self, method, prepared_url, headers, body = ''):
        method = method.lower()
        assert method in _METHODS, "Unknown method %s" % method

        future = _METHODS[method](prepared_url, headers = headers, data = body)
        res = ResultWrapper(self, method, prepared_url)
        self.requests_to_send.append(future)
        self.results.append(res)
        return res

    def wait_all_requests_completed(self):
        if len(self.requests_to_send) == 0:
            return
        try:
            for resp, result in zip(erequests.map(self.requests_to_send), self.results):
                result.response = resp
        finally:
            self.requests_to_send = []
            self.results = []
