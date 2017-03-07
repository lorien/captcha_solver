from six.moves.urllib.request import urlopen, Request
from six.moves.urllib.error import HTTPError
from six.moves.urllib.parse import urlencode


def request(url, data, timeout):
    if data:
        req_data = urlencode(data).encode('ascii')
    else:
        req_data = None
    req = Request(url, req_data)
    try:
        response = urlopen(req, timeout=timeout)
        body = response.read()
        code = response.getcode()
    except HTTPError as e:
        code = e.code
        body = e.fp.read()
    return {'code': code, 'body': body, 'url': url}
