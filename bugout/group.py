from typing import Any, Dict, Optional, Union
import uuid

from .calls import make_request
from .data import (
    Method,
    Role,
    BugoutGroup,
    BugoutGroupUser,
    BugoutGroupMembers,
    BugoutUserGroups,
    BugoutApplication,
    BugoutApplications,
)
from .exceptions import InvalidUrlSpec, GroupInvalidParameters
from .settings import REQUESTS_TIMEOUT


class Group:
    """
    Represent a group from Bugout.
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

    def get_group(
        self, token: Union[str, uuid.UUID], group_id: Union[str, uuid.UUID]
    ) -> BugoutGroup:
        get_group_path = f"group/{group_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=get_group_path, headers=headers)
        return BugoutGroup(**result)

    def find_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
    ) -> BugoutGroup:
        find_group_path = f"groups/find"
        query_params = {"group_id": group_id}
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.get,
            path=find_group_path,
            params=query_params,
            headers=headers,
        )
        return BugoutGroup(**result)

    def get_user_groups(self, token: Union[str, uuid.UUID]) -> BugoutUserGroups:
        get_user_groups_path = "groups"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.get, path=get_user_groups_path, headers=headers
        )
        return BugoutUserGroups(**result)

    def create_group(
        self, token: Union[str, uuid.UUID], group_name: str
    ) -> BugoutGroup:
        create_group_path = "group"
        data = {
            "group_name": group_name,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.post, path=create_group_path, headers=headers, data=data
        )
        return BugoutGroup(**result)

    def set_user_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        user_type: Role,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> BugoutGroupUser:
        set_user_group_path = f"group/{group_id}/role"

        if username is None and email is None:
            raise GroupInvalidParameters(
                "In order to update group role, at least one of username, or email must be specified"
            )

        data: Dict[str, Any] = {
            "user_type": user_type.value,
        }
        if username is not None:
            data.update({"username": username})
        if email is not None:
            data.update({"email": email})
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.post, path=set_user_group_path, headers=headers, data=data
        )
        return BugoutGroupUser(**result)

    def delete_user_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> BugoutGroupUser:
        """
        TODO(kompotkot): Merge with set_user_group()
        """
        delete_user_group_path = f"group/{group_id}/role"

        if username is None and email is None:
            raise GroupInvalidParameters(
                "In order to update group role, at least one of username, or email must be specified"
            )

        data = {}
        if username is not None:
            data.update({"username": username})
        if email is not None:
            data.update({"email": email})
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.delete,
            path=delete_user_group_path,
            headers=headers,
            data=data,
        )
        return BugoutGroupUser(**result)

    def get_group_members(
        self, token: Union[str, uuid.UUID], group_id: Union[str, uuid.UUID]
    ) -> BugoutGroupMembers:
        get_group_members_path = f"group/{group_id}/users"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.get, path=get_group_members_path, headers=headers
        )
        return BugoutGroupMembers(**result)

    def update_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        group_name: str,
    ) -> BugoutGroup:
        update_group_path = f"group/{group_id}/name"
        data = {
            "group_name": group_name,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.put, path=update_group_path, headers=headers, data=data
        )
        return BugoutGroup(**result)

    def delete_group(
        self, token: Union[str, uuid.UUID], group_id: Union[str, uuid.UUID]
    ) -> BugoutGroup:
        delete_group_path = f"group/{group_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.delete, path=delete_group_path, headers=headers
        )
        return BugoutGroup(**result)

    def create_application(
        self,
        token: Union[str, uuid.UUID],
        name: str,
        description: str,
        group_id: Union[str, uuid.UUID],
    ) -> BugoutApplication:
        applications_path = "applications"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        data = {
            "name": name,
            "description": description,
            "group_id": group_id,
        }
        result = self._call(
            method=Method.post, path=applications_path, headers=headers, data=data
        )
        return BugoutApplication(**result)

    def get_application(
        self,
        token: Union[str, uuid.UUID],
        application_id: Union[str, uuid.UUID],
    ) -> BugoutApplication:
        applications_path = f"applications/{application_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=applications_path, headers=headers)
        return BugoutApplication(**result)

    def list_applications(
        self,
        token: Union[str, uuid.UUID],
        group_id: Optional[Union[str, uuid.UUID]] = None,
    ) -> BugoutApplications:
        applications_path = "applications"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        query_params = {
            "group_id": group_id,
        }
        result = self._call(
            method=Method.get,
            path=applications_path,
            params=query_params,
            headers=headers,
        )
        return BugoutApplications(**result)

    def delete_application(
        self,
        token: Union[str, uuid.UUID],
        application_id: Union[str, uuid.UUID],
    ) -> BugoutApplication:
        applications_path = f"applications/{application_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.delete, path=applications_path, headers=headers
        )
        return BugoutApplication(**result)
