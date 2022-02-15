from sqlalchemy.orm import Session
from api.schemas.group import NamedGroupCreateRequest
from models.group import Group
from fastapi import HTTPException, status


def create_group(db: Session, name: str, affiliate_id: int) -> int:
    try:
        group = Group(
            name=name,
            affiliate_id=affiliate_id
        )

        db.add(group)
        db.commit()
        db.refresh(group)

        return group.id
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Server error')


def create_named_group(db: Session, request: NamedGroupCreateRequest, affiliate_id: int) -> int:
    try:
        group = Group(
            name=request.name,
            affiliate_id=affiliate_id,
            is_named=True
        )

        db.add(group)
        db.commit()
        db.refresh(group)

        return group.id
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Server error')


def get_groups(affiliate_id: int, db: Session):
    return db.query(Group).filter(Group.affiliate_id == affiliate_id).all()


def get_group_by_id(id: int, affiliate_id: int, db: Session):
    group = db.query(Group).filter_by(id=id, affiliate_id=affiliate_id).first()

    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Groups not found')

    return group
