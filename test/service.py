from captcha_solver import CaptchaSolver, CaptchaServiceError, ServiceTooBusy, BalanceTooLow
from unittest import TestCase
from mock import patch
from urlparse import urljoin
from grab import Grab
import logging
logging.basicConfig(level=logging.DEBUG)


@patch.object(Grab, 'request', autospec=True)
class AntigateBackendTestCase(TestCase):
    def setUp(self):
        self.domain = 'http://antigate.com'
        self.solver = CaptchaSolver('antigate', domain=self.domain, api_key='does not matter')

    def test_antigate_decoded(self, mock_request):
        def request(g):
            submit_url = urljoin(self.domain, 'in.php')
            check_url = urljoin(self.domain, 'res.php')
            if g.config['url'] == submit_url:
                g.response.body = 'OK|captcha_id'
                g.response.code = 200
            elif g.config['url'].startswith(check_url):
                g.response.code = 200
                g.response.body = 'OK|decoded_captcha'
        mock_request.side_effect = request

        self.assertEqual(self.solver.solve_captcha('image_data'), 'decoded_captcha')

    def test_antigate_no_slot_available(self, mock_request):
        def request(g):
            submit_url = urljoin(self.domain, 'in.php')
            if g.config['url'] == submit_url:
                g.response.body = 'ERROR_NO_SLOT_AVAILABLE'
                g.response.code = 200
        mock_request.side_effect = request

        self.assertRaises(ServiceTooBusy, self.solver.solve_captcha, 'image_data')

    def test_antigate_zero_balance(self, mock_request):
        def request(g):
            submit_url = urljoin(self.domain, 'in.php')
            if g.config['url'] == submit_url:
                g.response.body = 'ERROR_ZERO_BALANCE'
                g.response.code = 200
        mock_request.side_effect = request

        self.assertRaises(BalanceTooLow, self.solver.solve_captcha, 'image_data')


class TWOCaptchaBackendTestCase(AntigateBackendTestCase):
    def setUp(self):
        self.domain = 'http://2captcha.com'
        self.solver = CaptchaSolver('antigate', domain=self.domain, api_key='does not matter')
