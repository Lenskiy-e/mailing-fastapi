from fastapi import APIRouter, Depends
from schemas.group import GroupCreateRequest, NamedGroupCreateRequest
from sqlalchemy.orm import Session
from db.database import get_db
from repositories import group, phone

router = APIRouter(
    prefix='/group',
    tags=['group']
)


@router.post('/')
def create_group(request: GroupCreateRequest, db: Session = Depends(get_db)):
    id = group.create_group(db, request)
    phone.create_phone(db, request.phones, id)

    return {
        'result': 'created',
        'id': id
    }


@router.post('/named')
def create_named_group(request: NamedGroupCreateRequest, db: Session = Depends(get_db)):
    id = group.create_named_group(db, request)
    phone.create_phone_with_name(db, request.phones, id)

    return {
        'result': 'created',
        'id': id
    }