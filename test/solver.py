from captcha_solver.error import *  # noqa
from captcha_solver import CaptchaSolver
from unittest import TestCase
from test_server import TestServer

NO_DELAY = {'recognition_time': 1,
            'recognition_delay': 0,
            'submiting_time': 1,
            'submiting_delay': 0}


class ServerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TestServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.setup_solver()
        self.server.reset()

    def setup_solver(self):
        pass


class AntigateUrllibTestCase(ServerTestCase):
    def setup_solver(self):
        self.solver = CaptchaSolver('antigate',
                                    network_backend='urllib',
                                    service_url=self.server.get_url(),
                                    api_key='does not matter')

    def test_antigate_decoded(self):
        self.server.response_once['post.data'] = b'OK|captcha_id'
        self.server.response_once['get.data'] = b'OK|decoded_captcha'
        self.assertEqual(self.solver.solve_captcha(b'image_data'),
                         'decoded_captcha')

    def test_antigate_no_slot_available(self):
        self.server.response_once['post.data'] = b'ERROR_NO_SLOT_AVAILABLE'
        self.assertRaises(SolutionTimeoutError, self.solver.solve_captcha,
                          b'image_data', **NO_DELAY)

    def test_antigate_zero_balance(self):
        self.server.response_once['post.data'] = b'ERROR_ZERO_BALANCE'
        self.assertRaises(BalanceTooLow, self.solver.solve_captcha,
                          b'image_data')

    def test_solution_timeout_error(self):
        self.server.response_once['post.data'] = b'OK|captcha_id'
        self.server.response_once['get.data'] = b'CAPCHA_NOT_READY'
        self.assertRaises(SolutionTimeoutError, self.solver.solve_captcha,
                          b'image_data', **NO_DELAY)


class AntigateGrabTestCase(AntigateUrllibTestCase):
    def setup_solver(self):
        self.solver = CaptchaSolver('antigate',
                                    network_backend='grab',
                                    service_url=self.server.get_url(),
                                    api_key='does not matter')
