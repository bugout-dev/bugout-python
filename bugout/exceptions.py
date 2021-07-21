from typing import Any, Optional


class InvalidUrlSpec(ValueError):
    """
    Raised when an invalid url is specified.
    """


class BugoutUnexpectedResponse(Exception):
    """
    Raised when Bugout server response is unexpected (e.g. unparseable).
    """


class BugoutResponseException(Exception):
    """
    Raised when Bugout server response with error.
    """

    def __init__(
        self,
        message,
        status_code: int,
        detail: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        if detail is not None:
            self.detail = detail


class TokenInvalidParameters(ValueError):
    """
    Raised when operations are applied to a token but invalid parameters are provided with which to
    specify that token.
    """


class GroupInvalidParameters(ValueError):
    """
    Raised when operations are applied to a group but invalid parameters are provided.
    """
