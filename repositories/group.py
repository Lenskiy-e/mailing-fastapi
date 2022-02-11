from sqlalchemy.orm import Session
from api.schemas.group import NamedGroupCreateRequest
from models.group import Group
from fastapi import HTTPException, status


def create_group(db: Session, name: str) -> int:
    try:
        group = Group(
            name=name,
            affiliate_id=61838
        )

        db.add(group)
        db.commit()
        db.refresh(group)

        return group.id
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Server error')


def create_named_group(db: Session, request: NamedGroupCreateRequest) -> int:
    try:
        group = Group(
            name=request.name,
            affiliate_id=61838,
            is_named=True
        )

        db.add(group)
        db.commit()
        db.refresh(group)

        return group.id
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Server error')