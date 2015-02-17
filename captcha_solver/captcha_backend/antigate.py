from tempfile import mkstemp
from base64 import b64encode
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


from captcha_solver.captcha_backend.base import CaptchaBackend
from captcha_solver import (CaptchaServiceError, ServiceTooBusy,
                                BalanceTooLow, SolutionNotReady)


class AntigateBackend(CaptchaBackend):
    def setup(self, api_key, service_url='http://antigate.com', **kwargs):
        self.api_key = api_key
        self.service_url = service_url

    def get_submit_captcha_request_data(self, data, **kwargs):
        post = {
            'key': self.api_key,
            'method': 'base64',
            'body': b64encode(data),
        }
        post.update(kwargs)
        url = urljoin(self.service_url, 'in.php')
        return {'url': url, 'post_data': post}

    def parse_submit_captcha_response(self, res):
        """
        Returns: string
        """
        if res['code'] == 200:
            if res['body'].startswith(b'OK|'):
                return res['body'].split(b'|', 1)[1].decode('ascii')
            elif res['body'] == b'ERROR_NO_SLOT_AVAILABLE':
                raise ServiceTooBusy('Service too busy')
            elif res['body'] == b'ERROR_ZERO_BALANCE':
                raise BalanceTooLow('Balance too low')
            else:
                raise CaptchaServiceError(res['body'])
        else:
            raise CaptchaServiceError('Returned HTTP code: %d' % res['code'])
        
    def get_check_solution_request_data(self, captcha_id):
        params = {'key': self.api_key, 'action': 'get', 'id': captcha_id}
        url = urljoin(self.service_url, 'res.php?%s' % urlencode(params))
        return {'url': url, 'post_data': None}

    def parse_check_solution_response(self, res):
        """
        Returns: string
        """
        if res['code'] == 200:
            if res['body'].startswith(b'OK|'):
                return res['body'].split(b'|', 1)[1].decode('ascii')
            elif res['body'] == b'CAPCHA_NOT_READY':
                raise SolutionNotReady('Solution not ready')
            else:
                raise CaptchaServiceError(res['body'])
        else:
            raise CaptchaServiceError('Returned HTTP code: %d' % res['code'])
