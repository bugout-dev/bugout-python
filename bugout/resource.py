from typing import Any, Dict, Optional, Union
import uuid

from .calls import make_request, InvalidUrlSpec
from .data import Method, BugoutResource, BugoutResources
from .settings import REQUESTS_TIMEOUT


class ResourceInvalidParameters(ValueError):
    """
    Raised when operations are applied to a resource but invalid parameters are provided.
    """


class Resource:
    """
    Represent a resources from Bugout.
    """

    def __init__(
        self, url: Optional[str] = None, timeout: float = REQUESTS_TIMEOUT
    ) -> None:
        if url is None:
            raise InvalidUrlSpec("Invalid brood url specified")
        self.url = url
        self.timeout = timeout

    def _call(self, method: Method, path: str, **kwargs):
        url = f"{self.url.rstrip('/')}/{path.rstrip('/')}"
        result = make_request(method=method, url=url, timeout=self.timeout, **kwargs)
        return result

    def create_resource(
        self,
        token: Union[str, uuid.UUID],
        application_id: Union[str, uuid.UUID],
        resource_data: Dict[str, Any],
    ) -> BugoutResource:
        resources_path = "resources"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        json_data = {
            "application_id": application_id,
            "resource_data": resource_data,
        }
        result = self._call(
            method=Method.post, path=resources_path, headers=headers, json=json_data
        )
        return BugoutResource(**result)

    def get_resource(
        self,
        token: Union[str, uuid.UUID],
        resource_id: Union[str, uuid.UUID],
    ) -> BugoutResource:
        resources_path = f"resources/{resource_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=resources_path, headers=headers)
        return BugoutResource(**result)

    def list_resources(
        self,
        token: Union[str, uuid.UUID],
        application_id: Optional[Union[str, uuid.UUID]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> BugoutResources:
        resources_path = "resources"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        if application_id is not None:
            params["application_id"] = application_id
        result = self._call(
            method=Method.get, path=resources_path, params=params, headers=headers
        )
        return BugoutResources(**result)

    def delete_resource(
        self,
        token: Union[str, uuid.UUID],
        resource_id: Union[str, uuid.UUID],
    ) -> BugoutResource:
        resources_path = f"resources/{resource_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.delete, path=resources_path, headers=headers)
        return BugoutResource(**result)
