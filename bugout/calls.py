from typing import Any, Dict

import requests

from .data import Method
from .exceptions import BugoutResponseException, BugoutUnexpectedResponse


def make_request(method: Method, url: str, **kwargs) -> Any:
    response_body = None
    try:
        r = requests.request(method.value, url=url, **kwargs)
        r.raise_for_status()
        response_body = r.json()
    except requests.exceptions.RequestException as e:
        exception_detail = r.json()
        raise BugoutResponseException(
            "An exception occurred at Bugout API side",
            status_code=r.status_code,
            detail=exception_detail["detail"]
            if exception_detail["detail"] is not None
            else None,
        )
    except Exception as e:
        raise BugoutUnexpectedResponse(f"{str(e)}")
    return response_body


def ping(url: str) -> Dict[str, Any]:
    url = f"{url.rstrip('/')}/ping"
    return make_request(Method.get, url)
