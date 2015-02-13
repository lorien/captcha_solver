try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import urllib2


class UrllibBackend(object):
    def request(self, url, data):
        if data:
            request = urllib2.Request(url, urlencode(data))
        else:
            request = urllib2.Request(url, None)
        response = urllib2.urlopen(request)
        response.body = response.read()
        return response