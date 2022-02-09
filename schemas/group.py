from pydantic import BaseModel
from typing import List
from schemas.phone import PhoneWithNameCreateRequest


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
    group_id: int


class CreateGroupByFileResponse(BaseModel):
    result: str
    group_id: int
    invalid: List[str]


class CreateNamedGroupByFileResponse(BaseModel):
    result: str
    group_id: int
    invalid: List[str]
