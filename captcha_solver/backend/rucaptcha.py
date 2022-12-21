from __future__ import annotations

from .twocaptcha import TwocaptchaBackend


class RucaptchaBackend(TwocaptchaBackend):
    def __init__(
        self,
        api_key: str,
        service_url: str = "https://rucaptcha.com",
    ) -> None:
        super().__init__(api_key=api_key, service_url=service_url)
