import logging
from typing import Any, Dict, List, Optional, Tuple

import requests

from .data import Method

logger = logging.getLogger(__name__)


class BugoutUnexpectedResponse(Exception):
    """
    Raised when Bugout server response is unexpected (e.g. unparseable).
    """


class ApiCalls:
    """
    Handle REST API requests.
    """

    @staticmethod
    def make_request(method: Method, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        response_body = None

        try:
            r = requests.request(method.value, url=url, **kwargs)
            r.raise_for_status()
            response_body = r.json()
        except Exception as e:
            logger.error(f"Exception {str(e)}")
            raise

        return response_body
