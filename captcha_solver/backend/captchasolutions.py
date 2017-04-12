from base64 import b64encode
from six.moves.urllib.parse import urlencode, urljoin

from .base import ServiceBackend
from ..error import (CaptchaServiceError, ServiceTooBusy,
                     BalanceTooLow, SolutionNotReady)


class CaptchaSolutionsBackend(ServiceBackend):
    def setup(self, api_key, secret_key, service_url='http://api.captchasolutions.com', **kwargs):
        self.api_key = api_key
		self.secret_key = secret_key
        self.service_url = service_url

    def get_submit_captcha_request_data(self, data, **kwargs):
        post = {
            'key': self.api_key,
			'secret': self.secret_key,
			'out': 'text',
            'p': 'base64',
            'captcha': b64encode(data).decode('ascii'),
        }
        post.update(kwargs)
        url = urljoin(self.service_url, 'solve')
        return {'url': url, 'post_data': post}

    def parse_submit_captcha_response(self, res):
        """
        Returns: string
        """
        if res['code'] == 200:
            return res['body']
        else:
            raise CaptchaServiceError('Returned HTTP code: %d' % res['code'])