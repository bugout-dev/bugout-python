import uuid
from typing import Any, Dict, List, Optional, Union

from . import data
from .calls import ping
from .group import Group
from .humbug import Humbug
from .journal import Journal, SearchOrder, TagsAction
from .resource import Resource
from .settings import BUGOUT_BROOD_URL, BUGOUT_SPIRE_URL, REQUESTS_TIMEOUT
from .user import User


class Bugout:
    def __init__(
        self,
        brood_api_url: str = BUGOUT_BROOD_URL,
        spire_api_url: str = BUGOUT_SPIRE_URL,
    ) -> None:
        self.brood_api_url = brood_api_url
        self.spire_api_url = spire_api_url

        self.user = User(self.brood_api_url)
        self.group = Group(self.brood_api_url)
        self.humbug = Humbug(self.spire_api_url)
        self.journal = Journal(self.spire_api_url)
        self.resource = Resource(self.brood_api_url)

    @property
    def brood_url(self):
        return self.brood_api_url

    @property
    def spire_url(self):
        return self.spire_api_url

    def brood_ping(self) -> Dict[str, str]:
        return ping(self.brood_api_url)

    def spire_ping(self) -> Dict[str, str]:
        return ping(self.spire_api_url)

    # User handlers
    def create_user(
        self,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        signature: Optional[str] = None,
        application_id: Optional[Union[str, uuid.UUID]] = None,
        timeout: float = REQUESTS_TIMEOUT,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutUser:
        self.user.timeout = timeout
        return self.user.create_user(
            username=username,
            email=email,
            password=password,
            signature=signature,
            application_id=application_id,
            **kwargs,
        )

    def get_user(
        self,
        token: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutUser:
        self.user.timeout = timeout
        return self.user.get_user(
            token=token,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def get_user_by_id(
        self,
        token: Union[str, uuid.UUID],
        user_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutUser:
        self.user.timeout = timeout
        return self.user.get_user_by_id(
            token=token, user_id=user_id, auth_type=data.AuthType[auth_type], **kwargs
        )

    def find_user(
        self,
        username: str,
        token: Union[str, uuid.UUID] = None,
        timeout: float = REQUESTS_TIMEOUT,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutUser:
        self.user.timeout = timeout
        return self.user.find_user(username=username, token=token, **kwargs)

    def confirm_email(
        self,
        token: Union[str, uuid.UUID],
        verification_code: str,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutUser:
        self.user.timeout = timeout
        return self.user.confirm_email(token=token, verification_code=verification_code)

    def restore_password(
        self, email: str, timeout: float = REQUESTS_TIMEOUT
    ) -> Dict[str, str]:
        self.user.timeout = timeout
        return self.user.restore_password(email=email)

    def reset_password(
        self,
        reset_id: Union[str, uuid.UUID],
        new_password: str,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutUser:
        self.user.timeout = timeout
        return self.user.reset_password(reset_id=reset_id, new_password=new_password)

    def change_password(
        self,
        token: Union[str, uuid.UUID],
        current_password: str,
        new_password: str,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutUser:
        self.user.timeout = timeout
        return self.user.change_password(
            token=token, current_password=current_password, new_password=new_password
        )

    def delete_user(
        self,
        token: Union[str, uuid.UUID],
        user_id: Union[str, uuid.UUID],
        password: Optional[str] = None,
        timeout: float = REQUESTS_TIMEOUT,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutUser:
        self.user.timeout = timeout
        return self.user.delete_user(
            token=token, user_id=user_id, password=password, **kwargs
        )

    # Token handlers
    def create_token(
        self,
        username: str,
        password: str,
        application_id: Optional[Union[str, uuid.UUID]] = None,
        token_note: Optional[str] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutToken:
        self.user.timeout = timeout
        return self.user.create_token(
            username=username,
            password=password,
            application_id=application_id,
            token_note=token_note,
        )

    def create_token_restricted(
        self,
        token: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutToken:
        self.user.timeout = timeout
        return self.user.create_token_restricted(token=token)

    def revoke_token(
        self,
        token: Union[str, uuid.UUID],
        target_token: Optional[Union[str, uuid.UUID]] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> uuid.UUID:
        self.user.timeout = timeout
        return self.user.revoke_token(token=token, target_token=target_token)

    def revoke_token_by_id(
        self, token: Union[str, uuid.UUID], timeout: float = REQUESTS_TIMEOUT
    ) -> uuid.UUID:
        self.user.timeout = timeout
        return self.user.revoke_token_by_id(token=token)

    def update_token(
        self,
        token: Union[str, uuid.UUID],
        token_type: Optional[Union[str, data.TokenType]] = None,
        token_note: Optional[str] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutToken:
        self.user.timeout = timeout
        return self.user.update_token(
            token=token,
            token_type=data.TokenType(token_type) if token_type is not None else None,
            token_note=token_note,
        )

    def get_token_types(
        self, token: Union[str, uuid.UUID], timeout: float = REQUESTS_TIMEOUT
    ) -> List[str]:
        self.user.timeout = timeout
        return self.user.get_token_types(token=token)

    def get_user_tokens(
        self,
        token: Union[str, uuid.UUID],
        active: Optional[bool] = None,
        token_type: Optional[Union[str, data.TokenType]] = None,
        restricted: Optional[bool] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutUserTokens:
        self.user.timeout = timeout
        return self.user.get_user_tokens(
            token=token,
            active=active,
            token_type=data.TokenType(token_type) if token_type is not None else None,
            restricted=restricted,
        )

    # Group handlers
    def get_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutGroup:
        self.group.timeout = timeout
        return self.group.get_group(token=token, group_id=group_id)

    def find_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutGroup:
        self.user.timeout = timeout
        return self.group.find_group(token=token, group_id=group_id)

    def get_user_groups(
        self, token: Union[str, uuid.UUID], timeout: float = REQUESTS_TIMEOUT
    ) -> data.BugoutUserGroups:
        self.group.timeout = timeout
        return self.group.get_user_groups(token=token)

    def create_group(
        self,
        token: Union[str, uuid.UUID],
        group_name: str,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutGroup:
        self.group.timeout = timeout
        return self.group.create_group(token=token, group_name=group_name)

    def set_user_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        user_type: Union[str, data.Role],
        username: Optional[str] = None,
        email: Optional[str] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutGroupUser:
        self.group.timeout = timeout
        return self.group.set_user_group(
            token=token,
            group_id=group_id,
            user_type=data.Role(user_type),
            username=username,
            email=email,
        )

    def delete_user_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        username: Optional[str] = None,
        email: Optional[str] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutGroupUser:
        self.group.timeout = timeout
        return self.group.delete_user_group(
            token=token, group_id=group_id, username=username, email=email
        )

    def get_group_members(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutGroupMembers:
        self.group.timeout = timeout
        return self.group.get_group_members(token=token, group_id=group_id)

    def update_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        group_name: str,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutGroup:
        self.group.timeout = timeout
        return self.group.update_group(
            token=token, group_id=group_id, group_name=group_name
        )

    def delete_group(
        self,
        token: Union[str, uuid.UUID],
        group_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutGroup:
        self.group.timeout = timeout
        return self.group.delete_group(token=token, group_id=group_id)

    # Application handlers
    def create_application(
        self,
        token: Union[str, uuid.UUID],
        name: str,
        description: str,
        group_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutApplication:
        self.group.timeout = timeout
        return self.group.create_application(
            token=token, name=name, description=description, group_id=group_id
        )

    def get_application(
        self,
        token: Union[str, uuid.UUID],
        application_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutApplication:
        self.group.timeout = timeout
        return self.group.get_application(token=token, application_id=application_id)

    def list_applications(
        self,
        token: Union[str, uuid.UUID],
        group_id: Optional[Union[str, uuid.UUID]] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutApplications:
        self.group.timeout = timeout
        return self.group.list_applications(token=token, group_id=group_id)

    def delete_application(
        self,
        token: Union[str, uuid.UUID],
        application_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutApplication:
        self.group.timeout = timeout
        return self.group.delete_application(token=token, application_id=application_id)

    # Resource handlers
    def create_resource(
        self,
        token: Union[str, uuid.UUID],
        application_id: Union[str, uuid.UUID],
        resource_data: Dict[str, Any],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutResource:
        self.resource.timeout = timeout
        return self.resource.create_resource(
            token=token, application_id=application_id, resource_data=resource_data
        )

    def get_resource(
        self,
        token: Union[str, uuid.UUID],
        resource_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutResource:
        self.resource.timeout = timeout
        return self.resource.get_resource(token=token, resource_id=resource_id)

    def list_resources(
        self,
        token: Union[str, uuid.UUID],
        params: Optional[Dict[str, Any]] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutResources:
        self.resource.timeout = timeout
        return self.resource.list_resources(token=token, params=params)

    def update_resource(
        self,
        token: Union[str, uuid.UUID],
        resource_id: Union[str, uuid.UUID],
        resource_data: Dict[str, Any],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutResource:
        self.resource.timeout = timeout
        return self.resource.update_resource(
            token=token, resource_id=resource_id, resource_data_update=resource_data
        )

    def delete_resource(
        self,
        token: Union[str, uuid.UUID],
        resource_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutResource:
        self.resource.timeout = timeout
        return self.resource.delete_resource(token=token, resource_id=resource_id)

    # Journal scopes handlers
    def list_scopes(
        self, token: Union[str, uuid.UUID], api: str, timeout: float = REQUESTS_TIMEOUT
    ) -> data.BugoutScopes:
        self.journal.timeout = timeout
        return self.journal.list_scopes(token=token, api=api)

    def get_journal_permissions(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        holder_ids: Optional[List[Union[str, uuid.UUID]]] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutJournalPermissions:
        self.journal.timeout = timeout
        return self.journal.get_journal_permissions(
            token=token, journal_id=journal_id, holder_ids=holder_ids
        )

    def get_journal_scopes(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutJournalScopeSpecs:
        self.journal.timeout = timeout
        return self.journal.get_journal_scopes(token=token, journal_id=journal_id)

    def update_journal_scopes(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        holder_type: Union[str, data.HolderType],
        holder_id: Union[str, uuid.UUID],
        permission_list: List[str],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutJournalScopeSpecs:
        self.journal.timeout = timeout
        return self.journal.update_journal_scopes(
            token=token,
            journal_id=journal_id,
            holder_type=data.HolderType(holder_type),
            holder_id=holder_id,
            permission_list=permission_list,
        )

    def delete_journal_scopes(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        holder_type: Union[str, data.HolderType],
        holder_id: Union[str, uuid.UUID],
        permission_list: List[str],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutJournalScopeSpecs:
        self.journal.timeout = timeout
        return self.journal.delete_journal_scopes(
            token=token,
            journal_id=journal_id,
            holder_type=data.HolderType(holder_type),
            holder_id=holder_id,
            permission_list=permission_list,
        )

    # Journal handlers
    def create_journal(
        self,
        token: Union[str, uuid.UUID],
        name: str,
        journal_type: Optional[Union[str, data.JournalTypes]] = None,
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournal:
        self.journal.timeout = timeout
        if journal_type is None:
            journal_type = data.JournalTypes.DEFAULT
        return self.journal.create_journal(
            token=token,
            name=name,
            journal_type=data.JournalTypes(journal_type),
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def list_journals(
        self,
        token: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournals:
        self.journal.timeout = timeout
        return self.journal.list_journals(
            token=token, auth_type=data.AuthType[auth_type], **kwargs
        )

    def get_journal(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournal:
        self.journal.timeout = timeout
        return self.journal.get_journal(
            token=token,
            journal_id=journal_id,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def update_journal(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        name: str,
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournal:
        self.journal.timeout = timeout
        return self.journal.update_journal(
            token=token,
            journal_id=journal_id,
            name=name,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def delete_journal(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournal:
        self.journal.timeout = timeout
        return self.journal.delete_journal(
            token=token,
            journal_id=journal_id,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    # Journal entries
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
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntry:
        self.journal.timeout = timeout
        return self.journal.create_entry(
            token=token,
            journal_id=journal_id,
            title=title,
            content=content,
            tags=tags,
            context_url=context_url,
            context_id=context_id,
            context_type=context_type,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def create_entries_pack(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entries: List[Dict[str, Any]],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntries:
        self.journal.timeout = timeout
        entries_obj = data.BugoutJournalEntriesRequest(
            entries=[data.BugoutJournalEntryRequest(**entry) for entry in entries]
        )
        return self.journal.create_entries_pack(
            token=token,
            journal_id=journal_id,
            entries=entries_obj,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def get_entry(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntry:
        self.journal.timeout = timeout
        return self.journal.get_entry(
            token=token,
            journal_id=journal_id,
            entry_id=entry_id,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def get_entries(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntries:
        self.journal.timeout = timeout
        return self.journal.get_entries(
            token=token,
            journal_id=journal_id,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def get_entry_content(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntryContent:
        self.journal.timeout = timeout
        return self.journal.get_entry_content(
            token=token,
            journal_id=journal_id,
            entry_id=entry_id,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def update_entry_content(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        title: str,
        content: str,
        timeout: float = REQUESTS_TIMEOUT,
        tags: Optional[List[str]] = None,
        tags_action: TagsAction = TagsAction.merge,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntryContent:
        self.journal.timeout = timeout
        return self.journal.update_entry_content(
            token=token,
            journal_id=journal_id,
            entry_id=entry_id,
            title=title,
            content=content,
            tags=tags,
            tags_action=tags_action,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def delete_entry(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntry:
        self.journal.timeout = timeout
        return self.journal.delete_entry(
            token=token,
            journal_id=journal_id,
            entry_id=entry_id,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    # Tags
    def get_most_used_tags(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> List[Any]:
        self.journal.timeout = timeout
        return self.journal.get_most_used_tags(token=token, journal_id=journal_id)

    def create_tags(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        tags: List[str],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> List[Any]:
        self.journal.timeout = timeout
        return self.journal.create_tags(
            token=token,
            journal_id=journal_id,
            entry_id=entry_id,
            tags=tags,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def get_tags(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntryTags:
        self.journal.timeout = timeout
        return self.journal.get_tags(
            token=token,
            journal_id=journal_id,
            entry_id=entry_id,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def update_tags(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        tags: List[str],
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> List[Any]:
        self.journal.timeout = timeout
        return self.journal.update_tags(
            token=token,
            journal_id=journal_id,
            entry_id=entry_id,
            tags=tags,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    def delete_tag(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        entry_id: Union[str, uuid.UUID],
        tag: str,
        timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutJournalEntryTags:
        self.journal.timeout = timeout
        return self.journal.delete_tag(
            token=token,
            journal_id=journal_id,
            entry_id=entry_id,
            tag=tag,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    # Search
    def search(
        self,
        token: Union[str, uuid.UUID],
        journal_id: Union[str, uuid.UUID],
        query: str,
        filters: Optional[List[str]] = None,
        limit: int = 10,
        offset: int = 0,
        content: bool = True,
        timeout: float = REQUESTS_TIMEOUT,
        order: SearchOrder = SearchOrder.DESCENDING,
        auth_type: str = data.AuthType.bearer.name,
        **kwargs: Dict[str, Any],
    ) -> data.BugoutSearchResults:
        self.journal.timeout = timeout
        return self.journal.search(
            token,
            journal_id,
            query,
            filters,
            limit,
            offset,
            content,
            order=order,
            auth_type=data.AuthType[auth_type],
            **kwargs,
        )

    # Public
    def check_journal_public(
        self,
        journal_id: Union[str, uuid.UUID],
        timeout: float = REQUESTS_TIMEOUT,
    ) -> bool:
        self.journal.timeout = timeout
        return self.journal.check_journal_public(journal_id=journal_id)

    # Humbug
    def get_humbug_integrations(
        self,
        token: Union[str, uuid.UUID],
        group_id: Optional[Union[str, uuid.UUID]] = None,
        timeout: float = REQUESTS_TIMEOUT,
    ) -> data.BugoutHumbugIntegrationsList:
        self.humbug.timeout = timeout
        return self.humbug.get_humbug_integrations(token=token, group_id=group_id)
