from __future__ import annotations

from abc import abstractmethod
from typing import Any

from ..network import NetworkRequest, NetworkResponse


class ServiceBackend:
    @abstractmethod
    def get_submit_captcha_request_data(
        self, data: bytes, **kwargs: Any
    ) -> NetworkRequest:
        raise NotImplementedError

    @abstractmethod
    def parse_submit_captcha_response(self, res: NetworkResponse) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_check_solution_request_data(self, captcha_id: str) -> NetworkRequest:
        raise NotImplementedError

    @abstractmethod
    def parse_check_solution_response(self, res: NetworkResponse) -> str:
        raise NotImplementedError
