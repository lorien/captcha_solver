import logging
import time
import socket

import six
from six.moves.urllib.error import URLError

from .error import (SolutionNotReady, SolutionTimeoutError,
                    ServiceTooBusy, InvalidServiceBackend)
from .network import request
from .backend.antigate import AntigateBackend
from .backend.rucaptcha import RucaptchaBackend
from .backend.browser import BrowserBackend
from .backend.gui import GuiBackend
from .backend.base import ServiceBackend

logger = logging.getLogger('captcha_solver')
BACKEND_ALIAS = {
    'antigate': AntigateBackend,
    'rucaptcha': RucaptchaBackend,
    'browser': BrowserBackend,
    'gui': GuiBackend,
}
DEFAULT_NETWORK_TIMEOUT = 5


class InvalidBackend(Exception):
    pass


class CaptchaSolver(object):
    """
    This class implements API to communicate with
    remote captcha solving service.
    """

    def __init__(self, backend, **kwargs):
        """
        :param backend: alias name of one of standard backends or
            class inherited from SolverBackend
        """
        self.backend = self._initialize_backend(backend)
        self.backend.setup(**kwargs)
        self.network_config = {}
        self.setup_network_config()

    def setup_network_config(self, timeout=DEFAULT_NETWORK_TIMEOUT):
        self.network_config['timeout'] = timeout

    def _initialize_backend(self, backend):
        if isinstance(backend, ServiceBackend):
            return backend()
        elif isinstance(backend, six.string_types):
            return BACKEND_ALIAS[backend]()
        else:
            raise InvalidServiceBackend('Invalid backend: %s' % backend)

    def submit_captcha(self, image_data, **kwargs):
        logger.debug('Submiting captcha')
        data = self.backend.get_submit_captcha_request_data(image_data,
                                                            **kwargs)
        response = request(data['url'], data['post_data'],
                           timeout=self.network_config['timeout'])
        return self.backend.parse_submit_captcha_response(response)

    def check_solution(self, captcha_id):
        """
        Raises:
        * SolutionNotReady
        * ServiceTooBusy
        """

        data = self.backend.get_check_solution_request_data(captcha_id)
        response = request(data['url'], data['post_data'],
                           timeout=self.network_config['timeout'])
        return self.backend.parse_check_solution_response(response)

    def solve_captcha(self, data, submiting_time=30, submiting_delay=3,
                      recognition_time=120, recognition_delay=5, **kwargs):

        assert submiting_delay > 0
        assert recognition_delay > 0

        for _ in range(0, submiting_time, submiting_delay):
            fail = None
            try:
                captcha_id = self.submit_captcha(image_data=data, **kwargs)
            except (ServiceTooBusy, URLError, socket.error) as ex:
                fail = ex
                time.sleep(submiting_delay)
            else:
                break
        else:
            if isinstance(fail, ServiceTooBusy):
                raise SolutionTimeoutError('Service has not available slots'
                                           ' after %s seconds'
                                           % submiting_time)
            else:
                raise SolutionTimeoutError('Service is not available.'
                                           ' Error: %s' % ex)

        for _ in range(0, recognition_time, recognition_delay):
            fail = None
            try:
                return self.check_solution(captcha_id)
            except (SolutionNotReady, ServiceTooBusy,
                    URLError, socket.error) as ex:
                fail = ex
                time.sleep(recognition_delay)
            else:
                break
        else:
            if isinstance(fail, (ServiceTooBusy, SolutionNotReady)):
                raise SolutionTimeoutError('Captcha is not ready after'
                                           ' %s seconds' % recognition_time)
            else:
                raise SolutionTimeoutError('Service is not available.'
                                           ' Error: %s' % ex)
