from unittest import TestCase
from mock import patch
from grab import Grab
try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
try:
    from urllib import addinfourl
except ImportError:
    from urllib.response import addinfourl
from captcha_solver.error import *
from captcha_solver import CaptchaSolver


class AntigateBackendUrllibTransportTestCase(TestCase):
    def setup_solver(self):
        self.service_url = 'http://antigate.com'
        self.solver = CaptchaSolver('antigate',
                                    network_backend='urllib',
                                    service_url=self.service_url,
                                    api_key='does not matter')

    def setUp(self):
        self.setup_solver()
        self.patcher = patch('captcha_solver.transport_backend.urllib_backend.urlopen')
        self.mock_urlopen = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_antigate_decoded(self):
        def urlopen(url, data=None, timeout=None):
            url = url.get_full_url()
            submit_url = urljoin(self.service_url, 'in.php')
            check_url = urljoin(self.service_url, 'res.php')
            if url == submit_url:
                return addinfourl(BytesIO(b'OK|captcha_id'), {}, url, 200)
            elif url.startswith(check_url):
                return addinfourl(BytesIO(b'OK|decoded_captcha'), {}, url, 200)
            else:
                raise Exception('Invalid test')

        self.mock_urlopen.side_effect = urlopen
        self.assertEqual(self.solver.solve_captcha(b'image_data'), 'decoded_captcha')

    def test_antigate_no_slot_available(self):
        def urlopen(url, data=None, timeout=None):
            url = url.get_full_url()
            submit_url = urljoin(self.service_url, 'in.php')
            if url == submit_url:
                return addinfourl(BytesIO(b'ERROR_NO_SLOT_AVAILABLE'), {}, url, 200)
            else:
                raise Exception('Invalid test')

        self.mock_urlopen.side_effect = urlopen
        self.assertRaises(ServiceTooBusy, self.solver.solve_captcha, b'image_data')

    def test_antigate_zero_balance(self):
        def urlopen(url, data=None, timeout=None):
            url = url.get_full_url()
            submit_url = urljoin(self.service_url, 'in.php')
            if url == submit_url:
                return addinfourl(BytesIO(b'ERROR_ZERO_BALANCE'), {}, url, 200)
            else:
                raise Exception('Invalid test')

        self.mock_urlopen.side_effect = urlopen
        self.assertRaises(BalanceTooLow, self.solver.solve_captcha, b'image_data')

    def test_solution_timeout_error(self):
        def urlopen(url, data=None, timeout=None):
            url = url.get_full_url()
            submit_url = urljoin(self.service_url, 'in.php')
            check_url = urljoin(self.service_url, 'res.php')
            if url == submit_url:
                return addinfourl(BytesIO(b'OK|captcha_id'), {}, url, 200)
            elif url.startswith(check_url):
                return addinfourl(BytesIO(b'CAPCHA_NOT_READY'), {}, url, 200)
            else:
                raise Exception('Invalid test')

        self.mock_urlopen.side_effect = urlopen
        self.assertRaises(SolutionTimeoutError, self.solver.solve_captcha,
                          b'image_data', recognition_time=1, delay=1)


class AntigateBackendGrabTransportTestCase(TestCase):
    def setup_solver(self):
        self.service_url = 'http://antigate.com'
        self.solver = CaptchaSolver('antigate',
                                    network_backend='grab',
                                    service_url=self.service_url,
                                    api_key='does not matter')

    def setUp(self):
        self.setup_solver()
        self.patcher = patch.object(Grab, 'request', autospec=True)
        self.mock_request = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_antigate_decoded(self):
        def request(g):
            submit_url = urljoin(self.service_url, 'in.php')
            check_url = urljoin(self.service_url, 'res.php')
            if g.config['url'] == submit_url:
                g.response.body = b'OK|captcha_id'
                g.response.code = 200
            elif g.config['url'].startswith(check_url):
                g.response.code = 200
                g.response.body = b'OK|decoded_captcha'
            else:
                raise Exception('Invalid test')

        self.mock_request.side_effect = request
        self.assertEqual(self.solver.solve_captcha(b'image_data'), 'decoded_captcha')

    def test_antigate_no_slot_available(self):
        def request(g):
            submit_url = urljoin(self.service_url, 'in.php')
            if g.config['url'] == submit_url:
                g.response.body = b'ERROR_NO_SLOT_AVAILABLE'
                g.response.code = 200
            else:
                raise Exception('Invalid test')

        self.mock_request.side_effect = request
        self.assertRaises(ServiceTooBusy, self.solver.solve_captcha, b'image_data')

    def test_antigate_zero_balance(self):
        def request(g):
            submit_url = urljoin(self.service_url, 'in.php')
            if g.config['url'] == submit_url:
                g.response.body = b'ERROR_ZERO_BALANCE'
                g.response.code = 200
            else:
                raise Exception('Invalid test')

        self.mock_request.side_effect = request
        self.assertRaises(BalanceTooLow, self.solver.solve_captcha, b'image_data')

    def test_solution_timeout_error(self):
        def request(g):
            submit_url = urljoin(self.service_url, 'in.php')
            check_url = urljoin(self.service_url, 'res.php')
            if g.config['url'] == submit_url:
                g.response.body = b'OK|captcha_id'
                g.response.code = 200
            elif g.config['url'].startswith(check_url):
                g.response.code = 200
                g.response.body = b'CAPCHA_NOT_READY'
            else:
                raise Exception('Invalid test')

        self.mock_request.side_effect = request
        self.assertRaises(SolutionTimeoutError, self.solver.solve_captcha,
                          b'image_data', recognition_time=1, delay=1)


class TWOCaptchaBackendGrabTransportTestCase(AntigateBackendGrabTransportTestCase):
    def setup_solver(self):
        self.service_url = 'http://2captcha.com'
        self.solver = CaptchaSolver('antigate',
                                    network_backend='grab',
                                    service_url=self.service_url,
                                    api_key='does not matter')


class TWOCaptchaBackendUrllibTransportTestCase(AntigateBackendUrllibTransportTestCase):
    def setup_solver(self):
        self.service_url = 'http://2captcha.com'
        self.solver = CaptchaSolver('antigate',
                                    network_backend='urllib',
                                    service_url=self.service_url,
                                    api_key='does not matter')
