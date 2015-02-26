from grab import Grab

from captcha_solver.error import *  # noqa
from captcha_solver import CaptchaSolver
from captcha_solver.contrib.grab.captcha import solve_captcha
from .base import NO_DELAY, BaseSolverTestCase


class GrabContribTestCase(BaseSolverTestCase):
    def setup_solver(self):
        self.solver = CaptchaSolver('antigate',
                                    network_backend='urllib',
                                    service_url=self.server.get_url(),
                                    api_key='does not matter')

    def test_antigate_decoded_from_grab(self):
        def handler():
            yield b'OK|captcha_id'
            yield b'OK|decoded_captcha'

        self.server.response['data'] = handler()
        g = Grab(b'image_data')
        self.assertEqual(solve_captcha(self.solver, g, **NO_DELAY),
                         'decoded_captcha')

    def test_antigate_decoded_from_url(self):
        def handler():
            yield b'image_data'
            yield b'OK|captcha_id'
            yield b'OK|decoded_captcha'

        self.server.response['data'] = handler()
        g = Grab()
        self.assertEqual(solve_captcha(self.solver, g, url=self.server.get_url(), **NO_DELAY),
                         'decoded_captcha')