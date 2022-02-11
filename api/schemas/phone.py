from pydantic import BaseModel
from typing import List


class PhoneWithNameCreateRequest(BaseModel):
    name: str
    phone: str


class PhoneListResponse(BaseModel):
    valid: List[str]
    invalid: List[str]
