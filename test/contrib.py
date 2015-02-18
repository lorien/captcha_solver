from captcha_solver.error import *  # noqa
from captcha_solver import CaptchaSolver
from captcha_solver.contrib.grab.captcha import solve_captcha
from grab import Grab

from .solver import ServerTestCase, NO_DELAY


class GrabContribTestCase(ServerTestCase):
    def setup_solver(self):
        self.solver = CaptchaSolver('antigate',
                                    network_backend='urllib',
                                    service_url=self.server.get_url(),
                                    api_key='does not matter')

    def test_antigate_decoded_from_grab(self):
        self.server.response_once['post.data'] = b'OK|captcha_id'
        self.server.response_once['get.data'] = b'OK|decoded_captcha'
        g = Grab(b'image_data')
        self.assertEqual(solve_captcha(self.solver, g, **NO_DELAY),
                         'decoded_captcha')
