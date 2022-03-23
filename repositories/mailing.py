from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from api.schemas.mailing import CreateMailing
from models.mailing import Mailing
from fastapi import HTTPException, status


def create(data: CreateMailing, db: Session):
    try:
        mailing = Mailing(
            affiliate_id=data.affiliate_id,
            name=data.name,
            alpha_name=data.alpha_name,
            group_id=data.group_id,
            message=data.message,
            scheduled_at=data.scheduled_at,
            status=data.status,
            parts_count=data.parts_count,
            cost=data.cost,
            roi=data.roi,
            payout_id=data.payout_id
        )

        db.add(mailing)
        db.commit()
        db.refresh(mailing)

        return mailing.id
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Server error')
