import logging
from typing import Any, Dict, List, Optional, Tuple

from .app import Bugout
from .data import Method

logger = logging.getLogger(__name__)


class JournalNotFound(Exception):
    """
    Raised on actions that involve journal which are not present in the database.
    """


class Journal(Bugout):
    """
    Represent a journal from Bugout.
    """

    def __init__(self, bugout: Bugout) -> None:
        super().__init__(bugout.url, bugout.port)

    def get_journal(self, journal_id: str, token: str) -> Optional[Dict[str, Any]]:
        get_journal_path = f"journals/{journal_id}"

        headers = {
            "Authorization": f"Bearer {token}",
        }

        result = super()._call(
            method=Method.get, path=get_journal_path, headers=headers
        )
        return result
