from unittest import TestCase
from copy import copy
import time

from six import string_types
from test_server import TestServer

from captcha_solver import error
from captcha_solver import CaptchaSolver

NO_DELAY = {'recognition_time': 1,
            'recognition_delay': 1,
            'submiting_time': 1,
            'submiting_delay': 1}


class BaseSolverTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TestServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.reset()


class AntigateTestCase(BaseSolverTestCase):
    def setUp(self):
        super(AntigateTestCase, self).setUp()
        self.solver = self.create_solver()

    def create_solver(self, **kwargs):
        config = { 
            'service_url': self.server.get_url(),
            'api_key': 'does not matter',
        }
        config.update(kwargs)
        return CaptchaSolver('antigate', **config)

    def test_post_data(self):
        data = b'foo'
        res = self.solver.backend.get_submit_captcha_request_data(data)
        body = res['post_data']['body']

        self.assertTrue(isinstance(body, string_types))

    def test_antigate_decoded(self):
        def handler():
            yield b'OK|captcha_id'
            yield b'OK|decoded_captcha'

        self.server.response['data'] = handler()
        self.assertEqual(self.solver.solve_captcha(b'image_data'),
                         'decoded_captcha')

    def test_antigate_no_slot_available(self):
        self.server.response_once['data'] = b'ERROR_NO_SLOT_AVAILABLE'
        self.assertRaises(error.SolutionTimeoutError,
                          self.solver.solve_captcha,
                          b'image_data', **NO_DELAY)

    def test_antigate_zero_balance(self):
        self.server.response_once['data'] = b'ERROR_ZERO_BALANCE'
        self.assertRaises(error.BalanceTooLow, self.solver.solve_captcha,
                          b'image_data')

    def test_antigate_unknown_error(self):
        self.server.response_once['data'] = b'UNKNOWN_ERROR'
        self.assertRaises(error.CaptchaServiceError, self.solver.solve_captcha,
                          b'image_data')

    def test_antigate_unknown_code(self):
        self.server.response_once['code'] = 404
        self.assertRaises(error.CaptchaServiceError, self.solver.solve_captcha,
                          b'image_data')

    def test_solution_timeout_error(self):
        def handler():
            yield b'OK|captcha_id'
            yield b'CAPCHA_NOT_READY'

        self.server.response['data'] = handler()
        self.assertRaises(error.SolutionTimeoutError,
                          self.solver.solve_captcha,
                          b'image_data', **NO_DELAY)

    def test_solution_unknown_error(self):
        def handler():
            yield b'OK|captcha_id'
            yield b'UNKNOWN_ERROR'

        self.server.response['data'] = handler()
        self.assertRaises(error.CaptchaServiceError, self.solver.solve_captcha,
                          b'image_data', **NO_DELAY)

    def test_solution_unknown_code(self):
        def handler():
            yield b'OK|captcha_id'

        self.server.response['data'] = handler()
        self.assertRaises(error.CaptchaServiceError, self.solver.solve_captcha,
                          b'image_data', **NO_DELAY)

    def test_network_error_while_sending_captcha(self):
        def handler():
            yield b'that would be timed out'
            yield b'OK|captcha_id'
            yield b'OK|decoded_captcha'

        solver = self.create_solver()
        solver.setup_network_config(timeout=1)
        self.server.response['data'] = handler()
        self.server.response_once['sleep'] = 1.005
        delays = copy(NO_DELAY)
        delays.update(dict(submiting_time=2, submiting_delay=1))
        solver.solve_captcha(b'image_data', **delays)

    def test_network_error_while_receiving_solution(self):

        class Callback(object):
            def __init__(self):
                self.step = 0

            def __call__(self, server):
                self.step += 1
                if self.step == 1:
                    server.write(b'OK|captcha_id')
                    server.finish()
                elif self.step in (2, 3, 4):
                    time.sleep(1.005)
                    server.write(b'that would be timed out')
                    server.finish()
                elif self.step > 4:
                    server.write(b'OK|solution')
                    server.finish()

        solver = self.create_solver()
        solver.setup_network_config(timeout=1)
        self.server.response['callback'] = Callback()
        delays = copy(NO_DELAY)
        delays.update(dict(submiting_time=2, submiting_delay=1,
                           recognition_time=4, recognition_delay=1))
        solution = solver.solve_captcha(b'image_data', **delays)
        assert solution == 'solution'
