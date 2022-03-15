from typing import Optional

from sqlalchemy.orm import Session
from api.schemas.group import NamedGroupCreateRequest
from models.group import Group
from fastapi import HTTPException, status
from repositories import phone as phone_repository


def create_group(db: Session, name: str, affiliate_id: int, description: Optional[str] = '') -> int:
    try:
        group = Group(
            name=name,
            affiliate_id=affiliate_id,
            description=description
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
            is_named=True,
            description=request.description
        )

        db.add(group)
        db.commit()
        db.refresh(group)

        return group.id
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Server error')


def get_groups(affiliate_id: int, db: Session):
    return db.query(Group).filter(Group.affiliate_id == affiliate_id).all()


def get_group_by_id(id: int, db: Session):
    group = get_group_instance_by_id(id, db).first()

    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Group not found')

    return group


def get_group_instance_by_id(id: int, db: Session):
    group = db.query(Group).filter(Group.id == id)

    if not group.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Group not found')

    return group


def group_exists(id: int, affiliate_id: int, db: Session) -> bool:
    return db.query(Group).filter_by(id=id, affiliate_id=affiliate_id).count()


def update_data(group: Group, db: Session, name: str, description: Optional[str] = '') -> None:
    group.update({
        Group.name: name,
        Group.description: description
    })
    db.commit()


def delete(group: Group, db: Session) -> None:
    for phone in group.phones:
        phone_repository.delete(phone, db)

    db.delete(group)
    db.commit()
