import urllib, json, datetime
from pytz import UTC


class RestException(Exception):
    def __init__(self, method, url, code, raw_body):
        super(RestException, self).__init__("An error has occurred during %s to %s. Status %s. Body %s" % (
                                                                                                           method,
                                                                                                           url,
                                                                                                           code,
                                                                                                           raw_body
                                                                                                           ))
        self.method = method
        self.url = url
        self.code = code
        self.raw_body = raw_body


def format_timestamp(ts):
    if ts.tzinfo:
        ts = UTC.normalize(ts)
    else:
        ts = ts.replace(tzinfo = UTC)
    return ts.isoformat()


def get_cur_time():
    return datetime.datetime.now(UTC)


class Signature(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


class ClientBase(object):
    def __init__(self, base_url, default_url_args = {}, default_query_args = {}, add_headers = {}, async = False):
        self.base_url = base_url.rstrip('/')
        self.default_url_args = default_url_args
        self.default_query_args = default_query_args
        self.headers = {
                        'Accept' : 'application/json',
                        'Content-type' : 'application/json'
                        }
        self.headers.update(add_headers)
        if async:
            from pyarc.backends.erequests_client import ERequestsClient
            self.impl = ERequestsClient()
        else:
            from pyarc.backends.requests_client import RequestsClient
            self.impl = RequestsClient()

    def _prepare_arg(self, arg):
        if isinstance(arg, unicode):
            return arg.encode('utf8')
        return str(arg)

    def _prepare_url_args(self, **args):
        return { k : urllib.quote_plus(self._prepare_arg(v)) for k, v in args.viewitems() }

    def _prepare_url(self, template, url_args, query_args):
        if template[0] != '/':
            template = '/' + template
        final_url_args = self.default_url_args.copy()
        final_url_args.update(self._prepare_url_args(**url_args))
        final_query_args = self.default_query_args.copy()
        final_query_args.update(query_args)
        result = self.base_url + template.format(**final_url_args)
        qs = urllib.urlencode(final_query_args)
        if qs:
            result += '?' + qs
        return result

    def do_req(self, method, url_template, url_args = {}, query_args = {}, body = ''):
        url = self._prepare_url(url_template, url_args, query_args)
        return self.impl.start_req(method, url, self.headers, body)

    def get(self, url_template, url_args = {}, query_args = {}):
        return self.do_req('get', url_template, url_args, query_args)

    def delete(self, url_template, url_args = {}, query_args = {}):
        return self.do_req('delete', url_template, url_args, query_args)

    def post(self, url_template, url_args = {}, payload = {}):
        return self.do_req('post', url_template, url_args, body = json.dumps(payload))

    def put(self, url_template, url_args = {}, payload = {}):
        return self.do_req('put', url_template, url_args, body = json.dumps(payload))

    def wait_all_requests_completed(self):
        self.impl.wait_all_requests_completed()

    def batch(self, signatures):
        futures = [s() for s in signatures]
        self.wait_all_requests_completed()
        return [f.get() for f in futures]
