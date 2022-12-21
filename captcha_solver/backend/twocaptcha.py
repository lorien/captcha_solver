from typing import Any

from ..network import NetworkRequest
from .antigate import AntigateBackend

SOFTWARE_ID = 2373


class TwocaptchaBackend(AntigateBackend):
    def __init__(
        self,
        api_key: str,
        service_url: str = "http://antigate.com",
    ) -> None:
        super().__init__(api_key=api_key, service_url=service_url)

    def get_submit_captcha_request_data(
        self, data: bytes, **kwargs: Any
    ) -> NetworkRequest:
        res = super().get_submit_captcha_request_data(data, **kwargs)
        assert res["post_data"] is not None
        res["post_data"]["soft_id"] = SOFTWARE_ID
        return res
