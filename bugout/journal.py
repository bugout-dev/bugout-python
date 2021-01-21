from typing import Any, Dict, List, Optional
import uuid

from .calls import make_request, InvalidUrlSpec
from .data import (
    BugoutJournal,
    BugoutJournals,
    BugoutScopes,
    BugoutJournalScopeSpecs,
    BugoutJournalEntry,
    BugoutJournalEntries,
    BugoutJournalEntryContent,
    BugoutJournalEntryTags,
    HolderType,
    Method,
)


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

    # Scope module
    def list_scopes(self, token: uuid.UUID, api: str) -> BugoutScopes:
        scopes_path = f"journals/scopes"
        json = {
            "api": api,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.get, path=scopes_path, headers=headers, json=json
        )
        print(result)
        return BugoutScopes(**result)

    def get_journal_scopes(
        self, token: uuid.UUID, journal_id: uuid.UUID
    ) -> BugoutJournalScopeSpecs:
        journal_scopes_path = f"journals/{journal_id}/scopes"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.get, path=journal_scopes_path, headers=headers
        )
        return BugoutJournalScopeSpecs(**result)

    def update_journal_scopes(
        self,
        token: uuid.UUID,
        journal_id: uuid.UUID,
        holder_type: HolderType,
        holder_id: uuid.UUID,
        permission_list: List[str],
    ) -> BugoutJournalScopeSpecs:
        journal_scopes_path = f"journals/{journal_id}/scopes"
        json = {
            "holder_type": holder_type,
            "holder_id": holder_id,
            "permission_list": permission_list,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.post, path=journal_scopes_path, headers=headers, json=json
        )
        return BugoutJournalScopeSpecs(**result)

    def delete_journal_scopes(
        self,
        token: uuid.UUID,
        journal_id: uuid.UUID,
        holder_type: HolderType,
        holder_id: uuid.UUID,
        permission_list: List[str],
    ) -> BugoutJournalScopeSpecs:
        journal_scopes_path = f"journals/{journal_id}/scopes"
        json = {
            "holder_type": holder_type,
            "holder_id": holder_id,
            "permission_list": permission_list,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.delete, path=journal_scopes_path, headers=headers, json=json
        )
        return BugoutJournalScopeSpecs(**result)

    # Journal module
    def create_journal(self, token: uuid.UUID, name: str) -> BugoutJournal:
        journal_path = "journals/"
        json = {
            "name": name,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.post, path=journal_path, headers=headers, json=json
        )
        return BugoutJournal(**result)

    def list_journals(self, token: uuid.UUID) -> BugoutJournals:
        journal_path = "journals/"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=journal_path, headers=headers)
        return BugoutJournals(**result)

    def get_journal(self, token: uuid.UUID, journal_id: uuid.UUID) -> BugoutJournal:
        journal_id_path = f"journals/{journal_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=journal_id_path, headers=headers)
        return BugoutJournal(**result)

    def update_journal(
        self, token: uuid.UUID, journal_id: uuid.UUID, name: str
    ) -> BugoutJournal:
        journal_id_path = f"journals/{journal_id}"
        json = {
            "name": name,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.put, path=journal_id_path, headers=headers, json=json
        )
        return BugoutJournal(**result)

    def delete_journal(self, token: uuid.UUID, journal_id: uuid.UUID) -> BugoutJournal:
        journal_id_path = f"journals/{journal_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.delete, path=journal_id_path, headers=headers)
        return BugoutJournal(**result)

    # Entry module
    def create_entry(
        self,
        token: uuid.UUID,
        journal_id: uuid.UUID,
        title: str,
        content: str,
        tags: List[str] = [],
        context_url: Optional[str] = None,
        context_id: Optional[str] = None,
        context_type: Optional[str] = None,
    ) -> BugoutJournalEntry:
        entry_path = f"journals/{journal_id}/entries"
        json = {
            "title": title,
            "content": content,
            "tags": tags,
            "context_url": context_url,
            "context_id": context_id,
            "context_type": context_type,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.post, path=entry_path, headers=headers, json=json
        )
        return BugoutJournalEntry(**result)

    def get_entry(
        self, token: uuid.UUID, journal_id: uuid.UUID, entry_id: uuid.UUID
    ) -> BugoutJournalEntry:
        entry_id_path = f"journals/{journal_id}/entries/{entry_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=entry_id_path, headers=headers)
        return BugoutJournalEntry(**result)

    def get_entries(
        self, token: uuid.UUID, journal_id: uuid.UUID
    ) -> BugoutJournalEntries:
        entry_path = f"journals/{journal_id}/entries"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=entry_path, headers=headers)
        return BugoutJournalEntries(**result)

    def get_entry_content(
        self, token: uuid.UUID, journal_id: uuid.UUID, entry_id: uuid.UUID
    ) -> BugoutJournalEntryContent:
        entry_id_content_path = f"journals/{journal_id}/entries/{entry_id}/content"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.get, path=entry_id_content_path, headers=headers
        )
        return BugoutJournalEntryContent(**result)

    def update_entry_content(
        self,
        token: uuid.UUID,
        journal_id: uuid.UUID,
        entry_id: uuid.UUID,
        title: str,
        content: str,
    ) -> BugoutJournalEntryContent:
        entry_id_content_path = f"journals/{journal_id}/entries/{entry_id}/content"
        json = {
            "title": title,
            "content": content,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.put,
            path=entry_id_content_path,
            headers=headers,
            json=json,
        )
        return BugoutJournalEntryContent(**result)

    def delete_entry(
        self,
        token: uuid.UUID,
        journal_id: uuid.UUID,
        entry_id: uuid.UUID,
    ) -> BugoutJournalEntry:
        entry_id_path = f"journals/{journal_id}/entries/{entry_id}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.delete, path=entry_id_path, headers=headers)
        return BugoutJournalEntry(**result)

    # Tags modules
    def get_most_used_tags(self, token: uuid.UUID, journal_id: uuid.UUID) -> List[Any]:
        tags_path = f"journals/{journal_id}/tags"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=tags_path, headers=headers)
        return result

    def create_tags(
        self,
        token: uuid.UUID,
        journal_id: uuid.UUID,
        entry_id: uuid.UUID,
        tags: List[str],
    ) -> List[Any]:
        tags_path = f"journals/{journal_id}/entries/{entry_id}/tags"
        json = {"tags": tags}
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.post, path=tags_path, headers=headers, json=json
        )
        return result

    def get_tags(
        self, token: uuid.UUID, journal_id: uuid.UUID, entry_id: uuid.UUID
    ) -> BugoutJournalEntryTags:
        tags_path = f"journals/{journal_id}/entries/{entry_id}/tags"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=tags_path, headers=headers)
        return BugoutJournalEntryTags(**result)

    def update_tags(
        self,
        token: uuid.UUID,
        journal_id: uuid.UUID,
        entry_id: uuid.UUID,
        tags: List[str],
    ) -> List[Any]:
        tags_path = f"journals/{journal_id}/entries/{entry_id}/tags"
        json = {"tags": tags}
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.put, path=tags_path, headers=headers, json=json
        )
        return result

    def delete_tag(
        self,
        token: uuid.UUID,
        journal_id: uuid.UUID,
        entry_id: uuid.UUID,
        tag: str,
    ) -> BugoutJournalEntryTags:
        tags_path = f"journals/{journal_id}/entries/{entry_id}/tags"
        json = {"tag": tag}
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(
            method=Method.delete, path=tags_path, headers=headers, json=json
        )
        return BugoutJournalEntryTags(**result)
