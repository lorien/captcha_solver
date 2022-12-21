from __future__ import annotations

import time
from unittest import TestCase

from test_server import Response, TestServer

from captcha_solver import CaptchaSolver, error

# These timings means the solver will do only
# one attempt to submit captcha and
# one attempt to receive solution
# Assuming the network timeout is greater than
# submiting/recognition delays
TESTING_TIME_PARAMS = {
    "submiting_time": 0.1,
    "submiting_delay": 0.2,
    "recognition_time": 0.1,
    "recognition_delay": 0.2,
}
TEST_SERVER_HOST = "127.0.0.1"


class BaseSolverTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TestServer(address=TEST_SERVER_HOST)
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.reset()


class AntigateTestCase(BaseSolverTestCase):
    def setUp(self):
        super().setUp()
        self.solver = self.create_solver()

    def create_solver(self, **kwargs):
        config = {
            "service_url": self.server.get_url(),
            "api_key": "does not matter",
        }
        config.update(kwargs)
        return CaptchaSolver("antigate", **config)

    def test_post_data(self):
        data = b"foo"
        res = self.solver.backend.get_submit_captcha_request_data(data)
        body = res["post_data"]["body"]

        self.assertTrue(isinstance(body, str))

    def test_antigate_decoded(self):
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"OK|decoded_captcha"))
        self.assertEqual(self.solver.solve_captcha(b"image_data"), "decoded_captcha")

    def test_antigate_no_slot_available(self):
        self.server.add_response(Response(data=b"ERROR_NO_SLOT_AVAILABLE"), count=-1)
        with self.assertRaises(error.SolutionTimeoutError):
            self.solver.solve_captcha(b"image_data", **TESTING_TIME_PARAMS)

    def test_antigate_zero_balance(self):
        self.server.add_response(Response(data=b"ERROR_ZERO_BALANCE"))
        self.assertRaises(error.BalanceTooLow, self.solver.solve_captcha, b"image_data")

    def test_antigate_unknown_error(self):
        self.server.add_response(Response(data=b"UNKNOWN_ERROR"))
        self.assertRaises(
            error.CaptchaServiceError, self.solver.solve_captcha, b"image_data"
        )

    def test_antigate_unknown_code(self):
        self.server.add_response(Response(status=404))
        self.assertRaises(
            error.CaptchaServiceError, self.solver.solve_captcha, b"image_data"
        )

    def test_solution_timeout_error(self):
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"CAPCHA_NOT_READY"))
        with self.assertRaises(error.SolutionTimeoutError):
            self.solver.solve_captcha(b"image_data", **TESTING_TIME_PARAMS)

    def test_solution_unknown_error(self):
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"UNKONWN_ERROR"))
        with self.assertRaises(error.CaptchaServiceError):
            self.solver.solve_captcha(b"image_data", **TESTING_TIME_PARAMS)

    def test_solution_unknown_code(self):
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"OK|solution", status=500))
        with self.assertRaises(error.CaptchaServiceError):
            self.solver.solve_captcha(b"image_data", **TESTING_TIME_PARAMS)

    def test_network_error_while_sending_captcha(self):
        self.server.add_response(Response(data=b"that would be timeout", sleep=0.2))
        self.server.add_response(Response(data=b"OK|captcha_id"))
        self.server.add_response(Response(data=b"OK|solution"))

        solver = self.create_solver()
        solver.setup_network_config(timeout=0.1)
        solver.solve_captcha(
            b"image_data",
            submiting_time=0.5,
            submiting_delay=0.15,
            recognition_time=0,
            recognition_delay=0,
        )

    def test_network_error_while_receiving_solution(self):
        class Callback:
            def __init__(self):
                self.step = 0

            def __call__(self):
                self.step += 1
                if self.step == 1:
                    return {
                        "type": "response",
                        "data": b"OK|captcha_id",
                    }
                if self.step in {2, 3, 4}:
                    time.sleep(0.2)
                    return {
                        "type": "response",
                        "data": b"that will be timeout",
                    }
                return {
                    "type": "response",
                    "data": b"OK|solution",
                }

        solver = self.create_solver()
        solver.setup_network_config(timeout=0.1)
        self.server.add_response(Response(callback=Callback()), count=-1)
        solution = solver.solve_captcha(
            b"image_data",
            submiting_time=0,
            submiting_delay=0,
            recognition_time=1,
            recognition_delay=0.09,
        )
        assert solution == "solution"
