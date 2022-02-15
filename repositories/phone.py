from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.group import Phone
from fastapi import HTTPException, status
from typing import List
from api.schemas.phone import PhoneWithNameCreateRequest


def create_phone(db: Session, phones: List[str], group_id: int):
    try:
        for phone in phones:
            new_phone = Phone(
                group_id=group_id,
                phone=phone.strip('+')
            )

            db.add(new_phone)
        db.commit()
    except IntegrityError as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Duplicate phone provided')
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Server error')


def create_phone_with_name(db: Session, phones: List[PhoneWithNameCreateRequest], group_id: int):
    try:
        for phone in phones:
            new_phone = Phone(
                group_id=group_id,
                phone=phone.phone.strip('+'),
                name=phone.name
            )

            db.add(new_phone)
            db.commit()
            db.refresh(new_phone)
    except IntegrityError as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Duplicate phone provided')
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Server error')


def delete(db: Session, id: int):
    phone = db.query(Phone).filter_by(id=id).first()

    if not phone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Phone with id {id} not found'
        )

    db.delete(phone)
    db.commit()
