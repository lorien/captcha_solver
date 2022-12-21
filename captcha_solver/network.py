from __future__ import annotations

import typing
from collections.abc import Mapping
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from typing_extensions import TypedDict


# pylint: disable=consider-alternative-union-syntax,deprecated-typing-alias
class NetworkRequest(TypedDict):
    url: str
    post_data: typing.Optional[typing.MutableMapping[str, str | float]]


# pylint: enable=consider-alternative-union-syntax,deprecated-typing-alias


class NetworkResponse(TypedDict):
    code: int
    body: bytes
    url: str


def request(
    url: str, data: None | Mapping[str, str | float], timeout: float
) -> NetworkResponse:
    req_data = urlencode(data).encode("ascii") if data else None
    req = Request(url, req_data)
    try:
        with urlopen(req, timeout=timeout) as resp:  # nosec B310
            body = resp.read()
            code = resp.getcode()
    except HTTPError as ex:
        code = ex.code
        body = ex.fp.read()
    return {
        "code": code,
        "body": body,
        "url": url,
    }
