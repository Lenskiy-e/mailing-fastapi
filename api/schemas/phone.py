from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class PhonesWithName(BaseModel):
    name: str
    phone: str


class PhoneResponse(BaseModel):
    id: int
    phone: int
    name: Optional[str]
    deleted: bool
    cdate: datetime

    class Config:
        orm_mode = True


class ParsedPhonesResponse(BaseModel):
    valid: List[int]
    invalid: Optional[List[str]]


class ParsedNamedPhonesResponse(BaseModel):
    valid: List[PhonesWithName]
    invalid: Optional[List[str]]
