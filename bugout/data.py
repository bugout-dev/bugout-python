from datetime import datetime
from enum import Enum, unique
from typing import Any, Dict, List, Optional, Set
import uuid

from pydantic import BaseModel, Field


@unique
class Method(Enum):
    delete = "delete"
    get = "get"
    post = "post"
    put = "put"


@unique
class Role(Enum):
    owner = "owner"
    member = "member"


@unique
class TokenType(Enum):
    bugout = "bugout"
    slack = "slack"
    github = "github"


@unique
class HolderType(Enum):
    user = "user"
    group = "group"


@unique
class IntegrationType(Enum):
    slack = "slack"
    github = "github"


class BugoutUser(BaseModel):
    id: uuid.UUID = Field(alias="user_id")
    username: str
    email: str
    normalized_email: str
    verified: bool
    autogenerated: bool
    created_at: datetime
    updated_at: datetime


class BugoutUserShort(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    user_type: Role


class BugoutToken(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    active: bool
    token_type: Optional[str]
    note: Optional[str]
    created_at: datetime
    updated_at: datetime


class BugoutUserTokens(BaseModel):
    user_id: uuid.UUID
    username: str
    tokens: List[BugoutToken] = Field(alias="token")


class BugoutUserIntegration(BaseModel):
    user_id: uuid.UUID
    integration_user_id: str
    access_token: Optional[str] = None
    team_ids: List[str] = Field(default_factory=list)
    integration_type = IntegrationType


class BugoutGroup(BaseModel):
    id: uuid.UUID
    group_name: Optional[str]
    autogenerated: bool


class BugoutGroupUser(BaseModel):
    group_id: uuid.UUID
    user_id: uuid.UUID
    user_type: str
    autogenerated: Optional[bool] = None
    group_name: Optional[str] = None


class BugoutUserGroups(BaseModel):
    groups: List[BugoutGroupUser]


class BugoutGroupMembers(BaseModel):
    id: uuid.UUID
    name: str
    users: List[BugoutUserShort]


class BugoutScope(BaseModel):
    api: str
    scope: str
    description: str


class BugoutScopes(BaseModel):
    scopes: List[BugoutScope]


class BugoutJournalScopeSpec(BaseModel):
    journal_id: uuid.UUID
    holder_type: HolderType
    holder_id: str
    permission: str


class BugoutJournalScopeSpecs(BaseModel):
    scopes: List[BugoutJournalScopeSpec]


class BugoutJournal(BaseModel):
    id: uuid.UUID
    bugout_user_id: uuid.UUID
    holder_ids: Set[uuid.UUID] = Field(default_factory=set)
    name: str
    created_at: datetime
    updated_at: datetime


class BugoutJournals(BaseModel):
    journals: List[BugoutJournal]


class BugoutJournalEntry(BaseModel):
    id: uuid.UUID
    journal_url: str
    content_url: Optional[str]
    title: Optional[str]
    content: Optional[str]
    tags: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    context_url: Optional[str]
    context_type: Optional[str]


class BugoutJournalEntries(BaseModel):
    entries: List[BugoutJournalEntry]


class BugoutJournalEntryContent(BaseModel):
    title: str
    content: str


class BugoutJournalEntryTags(BaseModel):
    journal_id: uuid.UUID
    entry_id: uuid.UUID
    tags: List[str]


class BugoutSearchFields(BaseModel):
    query: str = ""
    filters: Optional[List[str]] = None
    limit: int = 10
    offset: int = 0
    content: Optional[bool] = True


class BugoutSearchResult(BaseModel):
    entry_url: str
    content_url: str
    title: str
    content: Optional[str]
    tags: List[str]
    created_at: str
    updated_at: str
    score: float


class BugoutSearchResults(BaseModel):
    total_results: int
    offset: int
    next_offset: Optional[int]
    max_score: float
    results: List[BugoutSearchResult]
