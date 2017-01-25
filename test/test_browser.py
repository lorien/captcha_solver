from unittest import TestCase
from captcha_solver import CaptchaSolver
from mock import patch


class BrowserTestCase(TestCase):

    def setUp(self):
        self.solver = CaptchaSolver('browser')
        self.wb_patcher = patch('webbrowser.open')
        self.mock_wb_open = self.wb_patcher.start()
        self.raw_input_patcher = patch(
            'captcha_solver.backend.browser.input')
        self.mock_raw_input = self.raw_input_patcher.start()

    def tearDown(self):
        self.wb_patcher.stop()
        self.raw_input_patcher.stop()

    def test_captcha_decoded(self):
        self.mock_wb_open.return_value = None
        self.mock_raw_input.return_value = 'decoded_captcha'

        self.assertEqual(self.solver.solve_captcha(b'image_data'),
                         'decoded_captcha')
