from pydantic import BaseModel
from typing import List
from schemas.phone import PhoneWithNameCreateRequest


class GroupCreateRequest(BaseModel):
    name: str
    phones: List[str]


class NamedGroupCreateRequest(BaseModel):
    name: str
    phones: List[PhoneWithNameCreateRequest]