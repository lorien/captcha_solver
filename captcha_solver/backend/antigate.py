from base64 import b64encode
# pylint: disable=relative-import
from six.moves.urllib.parse import urlencode, urljoin
# pylint: enable=relative-import

from .base import ServiceBackend
from ..error import (CaptchaServiceError, ServiceTooBusy,
                     BalanceTooLow, SolutionNotReady)


SOFTWARE_ID = 901


class AntigateBackend(ServiceBackend):
    def __init__(self, *args, **kwargs):
        super(AntigateBackend, self).__init__(*args, **kwargs)
        self.api_key = None
        self.service_url = None

    # pylint: disable=arguments-differ
    def setup(self, api_key, service_url='http://antigate.com', **kwargs):
        self.api_key = api_key
        self.service_url = service_url
    # pylint: enable=arguments-differ

    def get_submit_captcha_request_data(self, data, **kwargs):
        post = {
            'key': self.api_key,
            'method': 'base64',
            'body': b64encode(data).decode('ascii'),
            'soft_id': SOFTWARE_ID,
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
                return res['body'].split(b'|', 1)[1].decode('utf8')
            elif res['body'] == b'CAPCHA_NOT_READY':
                raise SolutionNotReady('Solution is not ready')
            else:
                raise CaptchaServiceError(res['body'])
        else:
            raise CaptchaServiceError('Returned HTTP code: %d' % res['code'])
