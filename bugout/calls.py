from typing import Any, Dict

import requests

from .data import Method


class InvalidUrlSpec(ValueError):
    """
    Raised when an invalid url is specified.
    """


class BugoutUnexpectedResponse(Exception):
    """
    Raised when Bugout server response is unexpected (e.g. unparseable).
    """


def make_request(method: Method, url: str, **kwargs) -> Any:
    response_body = None
    try:
        r = requests.request(method.value, url=url, **kwargs)
        r.raise_for_status()
        response_body = r.json()
    except Exception as e:
        raise BugoutUnexpectedResponse(f"Exception {str(e)}")
    return response_body


def ping(url: str) -> Dict[str, Any]:
    url = f"{url.rstrip('/')}/ping"
    return make_request(Method.get, url)
