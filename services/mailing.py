import re
from sqlalchemy.orm import Session
from api.schemas.mailing import CreateMailing, CreateRequest
from models.mailing import MailingStatus
from exceptions.mailing import SmsLengthLimitExceeded
from config import settings
from repositories import group as group_repository
from services.internal_client import pay_for_sms
from api.schemas.affiliate import AuthData

cyrillic_count_grid = {
    70: 1,
    134: 2,
    201: 3,
    268: 4
}

latin_count_grid = {
    160: 1,
    306: 2,
    459: 3,
    612: 4
}


async def create_mailing(request: CreateRequest, db: Session, auth_data: AuthData) -> CreateMailing:
    parts_count = count_parts(request.message)
    cost = count_cost(parts_count, request.group_id, db)
    create_data = CreateMailing(
        name=request.name,
        alpha_name=request.alpha_name,
        group_id=request.group_id,
        message=request.message,
        scheduled_at=request.scheduled_at,
        affiliate_id=auth_data.affiliate_id,
        status=MailingStatus.new,
        parts_count=parts_count,
        cost=cost,
        roi=0,
        payout_id=pay_for_sms(cost, auth_data.auth_key)
    )

    return create_data


def count_parts(message: str) -> int:
    count_grid = latin_count_grid

    if re.search("[а-яА-Я]", message):
        count_grid = cyrillic_count_grid

    for symbols_limit in count_grid:
        if len(message) < symbols_limit:
            return count_grid[symbols_limit]

    raise SmsLengthLimitExceeded


def count_cost(parts_count: int, group_id: int, db: Session) -> float:
    phones = group_repository.get_active_phones(group_id, db)

    return parts_count * settings.sms_cost * len(phones)
