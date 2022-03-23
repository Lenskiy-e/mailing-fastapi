import datetime
from pydantic import BaseModel
from models.mailing import MailingStatus


class CreatedMailingResponse(BaseModel):
    id: int


class CreateRequest(BaseModel):
    name: str
    alpha_name: str
    group_id: int
    message: str
    scheduled_at: datetime.datetime


class CreateMailing(CreateRequest):
    affiliate_id: int
    status: MailingStatus
    parts_count: int
    cost: float
    roi: float
    payout_id: int
    affiliate_id: int
