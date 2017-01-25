from unittest import TestCase
from captcha_solver import CaptchaSolver
from mock import patch


class GuiTestCase(TestCase):

    def setUp(self):
        self.solver = CaptchaSolver('gui')
        self.cw_patcher = patch(
            'captcha_solver.backend.gui.CaptchaWindow')
        self.mock_cw = self.cw_patcher.start()

    def tearDown(self):
        self.cw_patcher.stop()

    def test_captcha_decoded(self):

        class MockCW(object):
            def __init__(self, path, solution):
                self.solution = solution
                self.solution.append('decoded_captcha')

            def main(self):
                pass

        self.mock_cw.side_effect = MockCW

        self.assertEqual(self.solver.solve_captcha(b'image_data'),
                         'decoded_captcha')
