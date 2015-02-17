try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request


class UrllibBackend(object):
    def request(self, url, data):
        if data:
            request = Request(url, urlencode(data))
        else:
            request = Request(url, None)
        response = urlopen(request)
        body = response.read()
        return {'code': response.getcode(), 'body': body}
