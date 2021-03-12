from typing import Any, Dict, List, Optional, Union
import uuid

from .calls import make_request, InvalidUrlSpec
from .data import Method, TokenType, BugoutUser, BugoutToken, BugoutUserTokens
from .settings import REQUESTS_TIMEOUT


class TokenInvalidParameters(ValueError):
    """
    Raised when operations are applied to a token but invalid parameters are provided with which to
    specify that token.
    """


class User:
    """
    Represent a user from Bugout.
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

    # User module
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        **kwargs: Dict[str, Any],
    ) -> BugoutUser:
        create_user_path = "user"
        data = {
            "username": username,
            "email": email,
            "password": password,
        }
        headers = {}
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.post, path=create_user_path, headers=headers, data=data
        )
        return BugoutUser(**result)

    def get_user(self, token: Union[str, uuid.UUID]) -> BugoutUser:
        get_user_path = "user"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=get_user_path, headers=headers)
        return BugoutUser(**result)

    def get_user_by_id(
        self, token: Union[str, uuid.UUID], user_id: Union[str, uuid.UUID]
    ) -> BugoutUser:
        get_user_by_id_path = f"user/{user_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.get, path=get_user_by_id_path, headers=headers
        )
        return BugoutUser(**result)

    def find_user(
        self,
        username: str,
        token: Union[str, uuid.UUID] = None,
        **kwargs: Dict[str, Any],
    ) -> BugoutUser:
        find_user_path = f"user/find?username={username}"
        headers = {}
        if token is not None:
            headers.update({"Authorization": f"Bearer {token}"})
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(method=Method.get, path=find_user_path, headers=headers)
        return BugoutUser(**result)

    def confirm_email(
        self, token: Union[str, uuid.UUID], verification_code: str
    ) -> BugoutUser:
        confirm_user_email_path = "confirm"
        data = {
            "verification_code": verification_code,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.post, path=confirm_user_email_path, headers=headers, data=data
        )
        return BugoutUser(**result)

    def restore_password(self, email: str) -> Dict[str, str]:
        restore_password_path = "password/restore"
        data = {
            "email": email,
        }
        result = self._call(method=Method.post, path=restore_password_path, data=data)
        return result

    def reset_password(
        self, reset_id: Union[str, uuid.UUID], new_password: str
    ) -> BugoutUser:
        reset_password_path = "password/reset"
        data = {
            "reset_id": reset_id,
            "new_password": new_password,
        }
        result = self._call(method=Method.post, path=reset_password_path, data=data)
        return BugoutUser(**result)

    def change_password(
        self, token: Union[str, uuid.UUID], current_password: str, new_password: str
    ) -> BugoutUser:
        change_password_path = "password/change"
        data = {
            "new_password": new_password,
            "current_password": current_password,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.post, path=change_password_path, headers=headers, data=data
        )
        return BugoutUser(**result)

    def delete_user(
        self,
        token: Union[str, uuid.UUID],
        user_id: Union[str, uuid.UUID],
        password: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> BugoutUser:
        delete_user_path = f"user/{user_id}"
        data = {}
        if password is not None:
            data.update({"password": password})
        headers = {
            "Authorization": f"Bearer {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.delete, path=delete_user_path, headers=headers, data=data
        )
        return BugoutUser(**result)

    # Token module
    def create_token(self, username: str, password: str) -> BugoutToken:
        create_token_path = "token"
        data = {
            "username": username,
            "password": password,
        }
        result = self._call(method=Method.post, path=create_token_path, data=data)
        return BugoutToken(**result)

    def create_token_restricted(self, token: Union[str, uuid.UUID]) -> BugoutToken:
        create_token_path = "token/restricted"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.post, path=create_token_path, headers=headers)
        return BugoutToken(**result)

    def revoke_token(
        self,
        token: Union[str, uuid.UUID],
        target_token: Optional[Union[str, uuid.UUID]] = None,
    ) -> uuid.UUID:
        revoke_token_path = "token"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        data = {}
        if target_token is not None:
            data.update({"target_token": target_token})
        result = self._call(
            method=Method.delete, path=revoke_token_path, headers=headers, data=data
        )
        return result

    def revoke_token_by_id(self, token: Union[str, uuid.UUID]) -> uuid.UUID:
        revoke_token_path = f"token/{token}"
        result = self._call(method=Method.delete, path=revoke_token_path)
        return result

    def update_token(
        self,
        token: Union[str, uuid.UUID],
        token_type: Optional[TokenType] = None,
        token_note: Optional[str] = None,
    ) -> BugoutToken:
        update_token_path = "token"

        if token_type is None and token_note is None:
            raise TokenInvalidParameters(
                "In order to update token, at least one of token_type, or token_note must be specified"
            )
        data: Dict[str, Any] = {"access_token": token}
        if token_type is not None:
            data.update({"token_type": token_type.value})
        if token_note is not None:
            data.update({"token_note": token_note})

        result = self._call(method=Method.put, path=update_token_path, data=data)
        return BugoutToken(**result)

    def get_token_types(self, token: Union[str, uuid.UUID]) -> List[str]:
        get_token_types_path = "token/types"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.get, path=get_token_types_path, headers=headers
        )
        return result

    def get_user_tokens(
        self,
        token: Union[str, uuid.UUID],
        active: Optional[bool] = None,
        token_type: Optional[TokenType] = None,
        restricted: Optional[bool] = None,
    ) -> BugoutUserTokens:
        get_user_tokens_path = "tokens"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        query_params = {}
        if active is not None:
            query_params.update({"active": str(int(active))})
        if token_type is not None:
            query_params.update({"token_type": token_type.value})
        if restricted is not None:
            query_params.update({"restricted": str(int(restricted))})
        result = self._call(
            method=Method.get,
            path=get_user_tokens_path,
            params=query_params,
            headers=headers,
        )
        return BugoutUserTokens(**result)
