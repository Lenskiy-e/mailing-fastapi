from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PhoneWithNameCreateRequest(BaseModel):
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

