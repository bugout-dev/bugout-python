import logging
from typing import Any, Dict, List, Optional, Tuple

from .app import Bugout
from .data import Method

logger = logging.getLogger(__name__)


class GroupNotFound(Exception):
    """
    Raised on actions that involve group which are not present in the database.
    """


class Group(Bugout):
    """
    Represent a group from Bugout.
    """

    def __init__(self, bugout: Bugout) -> None:
        super().__init__(bugout.url, bugout.port)

    def get_group(self, group_id: str, token: str) -> Optional[Dict[str, Any]]:
        get_group_path = f"groups/{group_id}"

        headers = {
            "Authorization": f"Bearer {token}",
        }

        result = super()._call(method=Method.get, path=get_group_path, headers=headers)
        return result
