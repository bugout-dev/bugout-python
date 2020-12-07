from enum import Enum, unique
from typing import Any, Dict, List, Optional, Tuple
import uuid

from pydantic import BaseModel


@unique
class Method(Enum):
    get = "get"
    post = "post"
    delete = "delete"


class BroodUser(BaseModel):
    id: uuid.UUID
    username: Optional[str]
    email: Optional[str]
    token: Optional[uuid.UUID]


class BroodGroup(BaseModel):
    id: uuid.UUID
    group_name: Optional[str]
