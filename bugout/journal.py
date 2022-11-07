import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .calls import make_request
from .data import (
    AuthType,
    BugoutJournal,
    BugoutJournalEntries,
    BugoutJournalEntriesRequest,
    BugoutJournalEntry,
    BugoutJournalEntryContent,
    BugoutJournalEntryTags,
    BugoutJournalPermissions,
    BugoutJournals,
    BugoutJournalScopeSpecs,
    BugoutScopes,
    BugoutSearchResults,
    HolderType,
    JournalTypes,
    Method,
)
from .exceptions import InvalidUrlSpec
from .settings import REQUESTS_TIMEOUT


class SearchOrder(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class TagsAction(Enum):
    """
    tags_action query parameter for PUT /{journal_id}/entries/{entry_id} requests.
    See Spire API implementation of that endpoint for more details:
    https://github.com/bugout-dev/spire/blob/cc748d45d0aa7e3350105810449ff4c14fa64ec9/spire/journal/api.py#L1249

    Corresponds to EntryUpdateTagActions enum in Spire:
    https://github.com/bugout-dev/spire/blob/cc748d45d0aa7e3350105810449ff4c14fa64ec9/spire/journal/data.py#L32
    """

    ignore = "ignore"
    replace = "replace"
    merge = "merge"


class Journal:
    """
    Represent a journal from Bugout.
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

    # Scope module
    def list_scopes(self, token: Union[str, uuid.UUID], api: str) -> BugoutScopes:
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
        return BugoutScopes(**result)

    def get_journal_permissions(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        holder_ids: Optional[List[Union[str, uuid.UUID]]] = None,
    ) -> BugoutJournalPermissions:
        journal_scopes_path = f"journals/{journal_id}/permissions"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        query_params = {}
        if holder_ids is not None:
            holder_ids_string = [str(holder_id) for holder_id in holder_ids]
            holder_ids_param = ",".join(holder_ids_string)
            query_params = {"holder_ids": holder_ids_param}
        result = self._call(
            method=Method.get,
            path=journal_scopes_path,
            params=query_params,
            headers=headers,
        )
        return BugoutJournalPermissions(**result)

    def get_journal_scopes(
        self, token: Union[str, uuid.UUID], journal_id: Union[str, uuid.UUID]
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
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        holder_type: HolderType,
        holder_id: Union[str, uuid.UUID],
        permission_list: List[str],
    ) -> BugoutJournalScopeSpecs:
        journal_scopes_path = f"journals/{journal_id}/scopes"
        json = {
            "holder_type": holder_type.value,
            "holder_id": str(holder_id),
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
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        holder_type: HolderType,
        holder_id: Union[str, uuid.UUID],
        permission_list: List[str],
    ) -> BugoutJournalScopeSpecs:
        journal_scopes_path = f"journals/{journal_id}/scopes"
        json = {
            "holder_type": holder_type.value,
            "holder_id": str(holder_id),
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
    def create_journal(
        self,
        token: Union[str, uuid.UUID],
        name: str,
        journal_type: JournalTypes,
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournal:
        journal_path = "journals/"
        json = {"name": name, "journal_type": journal_type.value}
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.post, path=journal_path, headers=headers, json=json
        )
        return BugoutJournal(**result)

    def list_journals(
        self,
        token: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournals:
        journal_path = "journals/"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(method=Method.get, path=journal_path, headers=headers)
        return BugoutJournals(**result)

    def get_journal(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournal:
        journal_id_path = f"journals/{journal_id}"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(method=Method.get, path=journal_id_path, headers=headers)
        return BugoutJournal(**result)

    def update_journal(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        name: str,
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournal:
        journal_id_path = f"journals/{journal_id}"
        json = {
            "name": name,
        }
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.put, path=journal_id_path, headers=headers, json=json
        )
        return BugoutJournal(**result)

    def delete_journal(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournal:
        journal_id_path = f"journals/{journal_id}"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(method=Method.delete, path=journal_id_path, headers=headers)
        return BugoutJournal(**result)

    # Entry module
    def create_entry(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        title: str,
        content: str,
        tags: List[str] = [],
        context_url: Optional[str] = None,
        context_id: Optional[str] = None,
        context_type: Optional[str] = None,
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
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
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.post, path=entry_path, headers=headers, json=json
        )
        return BugoutJournalEntry(**result)

    def create_entries_pack(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entries: BugoutJournalEntriesRequest,
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournalEntries:
        entry_path = f"journals/{journal_id}/bulk"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        json = {
            "entries": [
                {
                    "title": entry.title,
                    "content": entry.content,
                    "tags": entry.tags,
                    "context_url": entry.context_url,
                    "context_id": entry.context_id,
                    "context_type": entry.context_type,
                }
                for entry in entries.entries
            ]
        }
        result = self._call(
            method=Method.post, path=entry_path, headers=headers, json=json
        )
        return BugoutJournalEntries(**result)

    def get_entry(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournalEntry:
        entry_id_path = f"journals/{journal_id}/entries/{entry_id}"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(method=Method.get, path=entry_id_path, headers=headers)
        return BugoutJournalEntry(**result)

    def get_entries(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournalEntries:
        entry_path = f"journals/{journal_id}/entries"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(method=Method.get, path=entry_path, headers=headers)
        return BugoutJournalEntries(**result)

    def get_entry_content(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournalEntryContent:
        entry_id_content_path = f"journals/{journal_id}/entries/{entry_id}/content"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.get, path=entry_id_content_path, headers=headers
        )
        return BugoutJournalEntryContent(**result)

    def update_entry_content(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        tags_action: TagsAction = TagsAction.merge,
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournalEntryContent:
        entry_id_content_path = f"journals/{journal_id}/entries/{entry_id}/content"
        params: Dict[str, str] = {}
        json: Dict[str, Any] = {
            "title": title,
            "content": content,
        }
        if tags is not None:
            json["tags"] = tags
            params["tags_action"] = tags_action.value
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.put,
            path=entry_id_content_path,
            headers=headers,
            json=json,
            params=params,
        )
        return BugoutJournalEntryContent(**result)

    def delete_entry(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournalEntry:
        entry_id_path = f"journals/{journal_id}/entries/{entry_id}"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(method=Method.delete, path=entry_id_path, headers=headers)
        return BugoutJournalEntry(**result)

    # Tags module
    def get_most_used_tags(
        self, token: Union[str, uuid.UUID], journal_id: Union[str, uuid.UUID]
    ) -> List[Any]:
        tags_path = f"journals/{journal_id}/tags"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        result = self._call(method=Method.get, path=tags_path, headers=headers)
        return result

    def create_tags(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        tags: List[str],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> List[Any]:
        tags_path = f"journals/{journal_id}/entries/{entry_id}/tags"
        json = {"tags": tags}
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.post, path=tags_path, headers=headers, json=json
        )
        return result

    def get_tags(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournalEntryTags:
        tags_path = f"journals/{journal_id}/entries/{entry_id}/tags"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(method=Method.get, path=tags_path, headers=headers)
        return BugoutJournalEntryTags(**result)

    def update_tags(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        tags: List[str],
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> List[Any]:
        tags_path = f"journals/{journal_id}/entries/{entry_id}/tags"
        json = {"tags": tags}
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.put, path=tags_path, headers=headers, json=json
        )
        return result

    def delete_tag(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        tag: str,
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutJournalEntryTags:
        tags_path = f"journals/{journal_id}/entries/{entry_id}/tags"
        json = {"tag": tag}
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        result = self._call(
            method=Method.delete, path=tags_path, headers=headers, json=json
        )
        return BugoutJournalEntryTags(**result)

    # Search module
    def search(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        query: str,
        filters: Optional[List[str]] = None,
        limit: int = 10,
        offset: int = 0,
        content: bool = True,
        order: SearchOrder = SearchOrder.DESCENDING,
        auth_type: AuthType = AuthType.bearer,
        **kwargs: Dict[str, Any],
    ) -> BugoutSearchResults:
        search_path = f"journals/{journal_id}/search"
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        if "headers" in kwargs.keys():
            headers.update(kwargs["headers"])
        query_params = {
            "q": query,
            "filters": filters if filters is not None else [],
            "limit": limit,
            "offset": offset,
            "content": content,
            "order": order.value,
        }
        result = self._call(
            method=Method.get, path=search_path, params=query_params, headers=headers
        )
        return BugoutSearchResults(**result)

    # Public module
    def check_journal_public(self, journal_id: Union[str, uuid.UUID]) -> bool:
        journal_path = "public/check"
        query_params = {"journal_id": journal_id}
        result = self._call(method=Method.get, path=journal_path, params=query_params)
        return result
