from typing import Optional, Union
import uuid

from .calls import make_request
from .data import Method, BugoutHumbugIntegrationsList
from .exceptions import InvalidUrlSpec
from .settings import REQUESTS_TIMEOUT


class Humbug:
    """
    Represent a humbug from Bugout.
    """

    def __init__(
        self, url: Optional[str] = None, timeout: float = REQUESTS_TIMEOUT
    ) -> None:
        if url is None:
            raise InvalidUrlSpec("Invalid spire url specified")
        self.url = url
        self.timeout = timeout

    def _call(self, method: Method, path: str, **kwargs):
        url = f"{self.url.rstrip('/')}/{path.rstrip('/')}"
        result = make_request(method=method, url=url, timeout=self.timeout, **kwargs)
        return result

    def get_humbug_integrations(
        self,
        token: Union[str, uuid.UUID],
        group_id: Optional[Union[str, uuid.UUID]] = None,
    ) -> BugoutHumbugIntegrationsList:
        humbug_path = "humbug/integrations"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        query_params = {}
        if group_id is not None:
            query_params.update({"group_id": group_id})
        result = self._call(
            method=Method.get, path=humbug_path, params=query_params, headers=headers
        )
        return BugoutHumbugIntegrationsList(**result)
