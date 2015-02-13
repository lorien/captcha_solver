import logging

from grab.util.module import import_string
from captcha_solver.const import SOlVER_BACKEND_ALIAS
from captcha_solver.error import SolutionNotReady, SolutionTimeoutError
import time
logger = logging.getLogger('captcha_solver')


class CaptchaSolver(object):
    """
    This class implements API to communicate with
    remote captcha solving service.
    """

    def __init__(self, backend, **kwargs):
        if backend in SOlVER_BACKEND_ALIAS:
            backend_path = SOlVER_BACKEND_ALIAS[backend]
        else:
            backend_path = backend
        self.backend = import_string(backend_path)()
        self.backend.setup(**kwargs)

    def submit_captcha(self, data, **kwargs):
        logger.debug('Submiting captcha')
        g = self.backend.get_submit_captcha_request(data, **kwargs)
        g.request()
        return self.backend.parse_submit_captcha_response(g.response)

    def check_solution(self, captcha_id):
        """
        Raises:
        * SolutionNotReady
        * ServiceTooBusy
        """

        g = self.backend.get_check_solution_request(captcha_id)
        g.request()
        return self.backend.parse_check_solution_response(g.response)

    def solve_captcha(self, data, recognition_time=120, delay=5, **kwargs):
        g = self.backend.get_submit_captcha_request(data, **kwargs)
        g.request()
        captcha_id = self.backend.parse_submit_captcha_response(g.response)

        for _ in xrange(0, recognition_time/delay, delay):
            try:
                return self.check_solution(captcha_id)
            except SolutionNotReady:
                time.sleep(delay)
        else:
            raise SolutionTimeoutError