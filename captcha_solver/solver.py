from __future__ import annotations

import logging
import socket
import time
from copy import copy
from pprint import pprint  # pylint: disable=unused-import
from typing import Any
from urllib.error import URLError

from typing_extensions import TypedDict
try:
    import deathbycaptcha
except ImportError:
    deathbycaptcha = None

from .backend.antigate import AntigateBackend
from .backend.base import ServiceBackend
from .backend.browser import BrowserBackend
from .backend.rucaptcha import RucaptchaBackend
from .backend.twocaptcha import TwocaptchaBackend
from .error import (
    InvalidServiceBackend,
    ServiceTooBusy,
    SolutionNotReady,
    SolutionTimeoutError,
)
from .network import request

LOGGER = logging.getLogger("captcha_solver")
BACKEND_ALIAS: dict[str, type[ServiceBackend]] = {
    "2captcha": TwocaptchaBackend,
    "rucaptcha": RucaptchaBackend,
    "antigate": AntigateBackend,
    "browser": BrowserBackend,
}


class NetworkConfig(TypedDict):
    timeout: float


DEFAULT_NETWORK_CONFIG: NetworkConfig = {
    "timeout": 5,
}


class InvalidBackend(Exception):
    pass


class CaptchaSolver:
    """This class implements API to communicate with remote captcha solving service."""

    def __init__(self, backend: str | type[ServiceBackend], **kwargs: Any) -> None:
        """Create CaptchaSolver instance.

        Parameters
        ----------
        backend : string | ServiceBackend subclass
            Alias name of one of standard backends or class inherited from SolverBackend
        """
        backend_cls = self.get_backend_class(backend)
        self.backend = backend_cls(**kwargs)
        self.network_config: NetworkConfig = copy(DEFAULT_NETWORK_CONFIG)

    def setup_network_config(self, timeout: None | int = None) -> None:
        if timeout is not None:
            self.network_config["timeout"] = timeout

    def get_backend_class(
        self, alias: str | type[ServiceBackend]
    ) -> type[ServiceBackend]:
        if isinstance(alias, str):
            return BACKEND_ALIAS[alias]
        if issubclass(alias, ServiceBackend):
            return alias
        raise InvalidServiceBackend("Invalid backend alias: %s" % alias)

    def submit_captcha(self, image_data: bytes, **kwargs: Any) -> str:
        LOGGER.debug("Submiting captcha")
        data = self.backend.get_submit_captcha_request_data(image_data, **kwargs)
        # pprint(data['post_data'])
        # print('URL: %s' % data['url'])
        response = request(
            data["url"], data["post_data"], timeout=self.network_config["timeout"]
        )
        return self.backend.parse_submit_captcha_response(response)

    def check_solution(self, captcha_id: str) -> str:
        """Check if service has solved requested captcha.

        Raises
        ------
        - SolutionNotReady
        - ServiceTooBusy
        """
        data = self.backend.get_check_solution_request_data(captcha_id)
        response = request(
            data["url"],
            data["post_data"],
            timeout=self.network_config["timeout"],
        )
        return self.backend.parse_check_solution_response(response)

    def submit_captcha_with_retry(
        self, submiting_time: float, submiting_delay: float, data: bytes, **kwargs: Any
    ) -> str:
        fail: None | Exception = None
        start_time = time.time()
        while True:
            # pylint: disable=overlapping-except
            try:
                return self.submit_captcha(image_data=data, **kwargs)
            except (ServiceTooBusy, URLError, socket.error, TimeoutError) as ex:
                fail = ex
                if ((time.time() + submiting_delay) - start_time) > submiting_time:
                    break
                time.sleep(submiting_delay)
        if isinstance(fail, ServiceTooBusy):
            raise SolutionTimeoutError("Service has no available slots") from fail
        raise SolutionTimeoutError(
            "Could not access the service, reason: {}".format(fail)
        ) from fail

    def check_solution_with_retry(
        self, recognition_time: float, recognition_delay: float, captcha_id: str
    ) -> str:
        fail: None | Exception = None
        start_time = time.time()
        while True:
            # pylint: disable=overlapping-except
            try:
                return self.check_solution(captcha_id)
            except (
                SolutionNotReady,
                socket.error,
                TimeoutError,
                ServiceTooBusy,
                URLError,
            ) as ex:
                fail = ex
                if ((time.time() + recognition_delay) - start_time) > recognition_time:
                    break
                time.sleep(recognition_delay)
        if isinstance(fail, (ServiceTooBusy, SolutionNotReady)):
            raise SolutionTimeoutError(
                "Captcha is not ready after" " %s seconds" % recognition_time
            )
        raise SolutionTimeoutError("Service is not available." " Error: %s" % fail)

    def solve_captcha(
        self,
        data: bytes,
        submiting_time: float = 30,
        submiting_delay: float = 3,
        recognition_time: float = 120,
        recognition_delay: float = 5,
        **kwargs: Any,
    ) -> str:
        assert submiting_time >= 0
        assert submiting_delay >= 0
        assert recognition_time >= 0
        assert recognition_delay >= 0
        captcha_id = self.submit_captcha_with_retry(
            submiting_time, submiting_delay, data, **kwargs
        )
        return self.check_solution_with_retry(
            recognition_time, recognition_delay, captcha_id
        )

class DeathByCaptchaSolver(deathbycaptcha.HttpClient):
    """
    Official deathbycaptcha client interface modified to work the same as 
    the CaptchaSolver class
    """

    def solve_captcha(self, data, timeout, **kwargs):
        return self.decode(data, timeout, **kwargs)
