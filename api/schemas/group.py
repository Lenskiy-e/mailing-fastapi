from pydantic import BaseModel
from typing import List, Optional
from api.schemas.phone import PhoneWithNameCreateRequest


class GroupCreateRequest(BaseModel):
    name: str
    phones: List[str]


class NamedGroupCreateRequest(BaseModel):
    name: str
    phones: List[PhoneWithNameCreateRequest]


class CreateFromFileRequest(BaseModel):
    name: str


class CreateGroupResponse(BaseModel):
    result: str
    group_id: Optional[int]
    count: int
    invalid: List[str]
