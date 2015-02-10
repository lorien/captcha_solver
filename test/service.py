from captcha_solver import CaptchaService, CaptchaServiceError
from unittest import TestCase


class BasicTestCase(TestCase):
    def test_antigate_error(self):
        c = CaptchaService('antigate', api_key='WRONG_API_KEY')
        self.assertRaises(CaptchaServiceError, c.submit_captcha, 'some_image')
