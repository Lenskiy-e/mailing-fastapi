import datetime
from pydantic import BaseModel
from typing import List, Optional
from api.schemas.phone import PhonesWithName, PhoneResponse
from models.group import GroupStatus


class GroupCreateRequest(BaseModel):
    name: str
    description: Optional[str]
    phones: Optional[List[str]]


class NamedGroupCreateRequest(BaseModel):
    name: str
    description: Optional[str]
    phones: Optional[List[PhonesWithName]]


class CreateFromFileRequest(BaseModel):
    name: str


class CreateGroupResponse(BaseModel):
    result: str
    group_id: Optional[int]
    count: int
    invalid: List[str]


class GetGroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_named: bool
    is_funnel: bool
    status: GroupStatus
    cdate: datetime.datetime
    phones: List[PhoneResponse]

    class Config:
        orm_mode = True