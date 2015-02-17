# coding:utf8
import logging
import importlib
import time

from captcha_solver.const import SOLVER_BACKEND_ALIAS, TRANSPORT_BACKEND_ALIAS
from captcha_solver.error import SolutionNotReady, SolutionTimeoutError


logger = logging.getLogger('captcha_solver')


def import_string(path):
    module_path, cls_name = path.rsplit('.', 1)
    return getattr(importlib.import_module(module_path), cls_name)


class CaptchaSolver(object):
    """
    This class implements API to communicate with
    remote captcha solving service.
    """

    def __init__(self, captcha_backend, network_backend='urllib', **kwargs):
        captcha_backend_path = SOLVER_BACKEND_ALIAS.get(captcha_backend, captcha_backend)
        network_backend_path = TRANSPORT_BACKEND_ALIAS.get(network_backend, network_backend)
        self.captcha_backend = import_string(captcha_backend_path)()
        self.network_backend = import_string(network_backend_path)()
        self.captcha_backend.setup(**kwargs)

    def submit_captcha(self, image_data, **kwargs):
        logger.debug('Submiting captcha')
        data = self.captcha_backend.get_submit_captcha_request_data(image_data, **kwargs)
        response = self.network_backend.request(data['url'], data['post_data'])
        return self.captcha_backend.parse_submit_captcha_response(response)

    def check_solution(self, captcha_id):
        """
        Raises:
        * SolutionNotReady
        * ServiceTooBusy
        """

        data = self.captcha_backend.get_check_solution_request_data(captcha_id)
        response = self.network_backend.request(data['url'], data['post_data'])
        return self.captcha_backend.parse_check_solution_response(response)

    def solve_captcha(self, data, recognition_time=120, delay=5, **kwargs):
        captcha_id = self.submit_captcha(image_data=data)

        for _ in range(0, int(recognition_time / delay), delay):
            try:
                return self.check_solution(captcha_id)
            except SolutionNotReady:
                time.sleep(delay)
        else:
            raise SolutionTimeoutError("Captcha is not ready after %s seconds" % recognition_time)
