from six.moves.urllib.request import urlopen, Request
from six.moves.urllib.error import HTTPError
from six.moves.urllib.parse import urlencode


class UrllibBackend(object):
    def request(self, url, data):
        if data:
            request = Request(url, urlencode(data).encode('ascii'))
        else:
            request = Request(url, None)
        try:
            response = urlopen(request)
            body = response.read()
            code = response.getcode()
        except HTTPError as e:
            code = e.code
            body = e.fp.read()
        return {'code': code, 'body': body, 'url': url}
