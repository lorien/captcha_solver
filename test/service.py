from captcha_solver.error import *
from captcha_solver import CaptchaSolver
from unittest import TestCase
from mock import patch
from urlparse import urljoin
import logging
logging.basicConfig(level=logging.DEBUG)


class AntigateBackendTestCase(TestCase):
    def setup_solver(self):
        self.service_url = 'http://antigate.com'
        self.solver = CaptchaSolver('antigate', service_url=self.service_url, api_key='does not matter')

    def setUp(self):
        self.setup_solver()
        self.patcher = patch.object(self.solver.backend.Transport, 'request', autospec=True)
        self.mock_request = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_antigate_decoded(self):
        def request(g):
            submit_url = urljoin(self.service_url, 'in.php')
            check_url = urljoin(self.service_url, 'res.php')
            if g.config['url'] == submit_url:
                g.response.body = 'OK|captcha_id'
                g.response.code = 200
            elif g.config['url'].startswith(check_url):
                g.response.code = 200
                g.response.body = 'OK|decoded_captcha'
        self.mock_request.side_effect = request

        self.assertEqual(self.solver.solve_captcha('image_data'), 'decoded_captcha')

    def test_antigate_no_slot_available(self):
        def request(g):
            submit_url = urljoin(self.service_url, 'in.php')
            if g.config['url'] == submit_url:
                g.response.body = 'ERROR_NO_SLOT_AVAILABLE'
                g.response.code = 200
        self.mock_request.side_effect = request

        self.assertRaises(ServiceTooBusy, self.solver.solve_captcha, 'image_data')

    def test_antigate_zero_balance(self):
        def request(g):
            submit_url = urljoin(self.service_url, 'in.php')
            if g.config['url'] == submit_url:
                g.response.body = 'ERROR_ZERO_BALANCE'
                g.response.code = 200
        self.mock_request.side_effect = request

        self.assertRaises(BalanceTooLow, self.solver.solve_captcha, 'image_data')

    def test_solution_timeout_error(self):
        def request(g):
            submit_url = urljoin(self.service_url, 'in.php')
            check_url = urljoin(self.service_url, 'res.php')
            if g.config['url'] == submit_url:
                g.response.body = 'OK|captcha_id'
                g.response.code = 200
            elif g.config['url'].startswith(check_url):
                g.response.code = 200
                g.response.body = 'CAPCHA_NOT_READY'
        self.mock_request.side_effect = request

        self.assertRaises(SolutionTimeoutError, self.solver.solve_captcha, 'image_data', recognition_time=1, delay=1)


class TWOCaptchaBackendTestCase(AntigateBackendTestCase):
    def setup_solver(self):
        self.service_url = 'http://2captcha.com'
        self.solver = CaptchaSolver('antigate', service_url=self.service_url, api_key='does not matter')
