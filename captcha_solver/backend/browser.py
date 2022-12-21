from __future__ import annotations

import os
import tempfile
import time
import webbrowser
from typing import Any

from ..network import NetworkRequest, NetworkResponse
from .base import ServiceBackend


class BrowserBackend(ServiceBackend):
    def setup(self, **_kwargs: Any) -> None:
        pass

    def get_submit_captcha_request_data(
        self, data: bytes, **kwargs: Any
    ) -> NetworkRequest:
        fd, path = tempfile.mkstemp()
        with open(path, "wb") as out:
            out.write(data)
        os.close(fd)
        url = "file://" + path
        return {"url": url, "post_data": None}

    def parse_submit_captcha_response(self, res: NetworkResponse) -> str:
        return res["url"].replace("file://", "")

    def get_check_solution_request_data(self, captcha_id: str) -> NetworkRequest:
        url = "file://" + captcha_id
        return {"url": url, "post_data": None}

    def parse_check_solution_response(self, res: NetworkResponse) -> str:
        webbrowser.open(url=res["url"])
        # Wait some time, skip some debug messages
        # which browser could dump to console
        time.sleep(0.5)
        path = res["url"].replace("file://", "")
        os.unlink(path)
        return input("Enter solution: ")
