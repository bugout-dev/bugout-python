import logging
from typing import Any, Dict, List, Optional, Tuple
import uuid

from .calls import make_request, InvalidUrlSpec
from .data import BugoutJournal, Method

logger = logging.getLogger(__name__)


class JournalNotFound(Exception):
    """
    Raised on actions that involve journal which are not present in the database.
    """


class Journal:
    """
    Represent a journal from Bugout.
    """

    def __init__(self, url: Optional[str] = None) -> None:
        if url is None:
            raise InvalidUrlSpec("Invalid spire url specified")
        self.url = url

    def _call(self, method: Method, path: str, **kwargs):
        url = f"{self.url.rstrip('/')}/{path.rstrip('/')}"
        result = make_request(method=method, url=url, **kwargs)
        return result

    def get_journal(self, journal_id: uuid.UUID, token: uuid.UUID) -> BugoutJournal:
        get_group_path = f"journals/{journal_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=get_group_path, headers=headers)
        return BugoutJournal(
            id=result.get("id"),
            bugout_user_id=result.get("bugout_user_id"),
            holder_ids=result.get("holder_ids"),
            name=result.get("name"),
            created_at=result.get("created_at"),
            updated_at=result.get("updated_at"),
        )
