from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from repositories import phone as phone_repository, group as group_repository
from services.internal_client import get_affiliate_id
from exceptions import group as group_exceptions

router = APIRouter(
    prefix='/phone',
    tags=['phone']
)


@router.delete('/{id}')
def delete(
        id: int,
        db: Session = Depends(get_db),
        affiliate_id: int = Depends(get_affiliate_id)
):
    phone = phone_repository.get_by_id(id, db)
    group = group_repository.get_group_by_id(phone.group_id, db)

    if not group.has_affiliate(affiliate_id):
        raise group_exceptions.GroupBelongsToAffiliateException(group.id, affiliate_id)

    phone_repository.delete(phone, db)

    return {
        'result': 'deleted'
    }
