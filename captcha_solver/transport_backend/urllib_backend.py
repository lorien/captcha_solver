try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

try:
    from urllib2 import HTTPError
except ImportError:
    from urllib.error import HTTPError


class UrllibBackend(object):
    def request(self, url, data):
        if data:
            request = Request(url, urlencode(data).encode('utf8'))
        else:
            request = Request(url, None)
        try:
            response = urlopen(request)
            body = response.read()
            code = response.getcode()
        except HTTPError as e:
            code = e.code
            body = e.fp.read()
        return {'code': code, 'body': body}
