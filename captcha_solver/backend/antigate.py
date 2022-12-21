from __future__ import annotations

from base64 import b64encode
from typing import Any
from urllib.parse import urlencode, urljoin

from ..error import BalanceTooLow, CaptchaServiceError, ServiceTooBusy, SolutionNotReady
from ..network import NetworkRequest, NetworkResponse
from .base import ServiceBackend

SOFTWARE_ID = 901


class AntigateBackend(ServiceBackend):
    def __init__(
        self,
        api_key: str,
        service_url: str = "http://antigate.com",
    ) -> None:
        super().__init__()
        self.api_key: None | str = api_key
        self.service_url: None | str = service_url

    def get_submit_captcha_request_data(
        self, data: bytes, **kwargs: Any
    ) -> NetworkRequest:
        assert self.api_key is not None
        post: dict[str, str | float] = {
            "key": self.api_key,
            "method": "base64",
            "body": b64encode(data).decode("ascii"),
            "soft_id": SOFTWARE_ID,
        }
        post.update(kwargs)
        assert self.service_url is not None
        url = urljoin(self.service_url, "in.php")
        return {"url": url, "post_data": post}

    def parse_submit_captcha_response(self, res: NetworkResponse) -> str:
        if res["code"] == 200:
            if res["body"].startswith(b"OK|"):
                return res["body"].split(b"|", 1)[1].decode("ascii")
            if res["body"] == b"ERROR_NO_SLOT_AVAILABLE":
                raise ServiceTooBusy("Service too busy")
            if res["body"] == b"ERROR_ZERO_BALANCE":
                raise BalanceTooLow("Balance too low")
            raise CaptchaServiceError(res["body"])
        raise CaptchaServiceError("Returned HTTP code: %d" % res["code"])

    def get_check_solution_request_data(self, captcha_id: str) -> NetworkRequest:
        assert self.api_key is not None
        assert self.service_url is not None
        params = {"key": self.api_key, "action": "get", "id": captcha_id}
        url = urljoin(self.service_url, "res.php?%s" % urlencode(params))
        return {"url": url, "post_data": None}

    def parse_check_solution_response(self, res: NetworkResponse) -> str:
        if res["code"] == 200:
            if res["body"].startswith(b"OK|"):
                return res["body"].split(b"|", 1)[1].decode("utf8")
            if res["body"] == b"CAPCHA_NOT_READY":
                raise SolutionNotReady("Solution is not ready")
            raise CaptchaServiceError(res["body"])
        raise CaptchaServiceError("Returned HTTP code: %d" % res["code"])
