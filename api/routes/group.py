import asyncio
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, Header
from api.schemas import group as group_schema
from sqlalchemy.orm import Session
from db.database import get_db
from repositories import group, phone
from services import phones_parser, internal_client

STATUS_CREATED = 'Crated'
STATUS_FAILED = 'Failed'

router = APIRouter(
    prefix='/group',
    tags=['group']
)


def get_affiliate_id(auth_key: Optional[str] = Header(None)):
    return asyncio.run(internal_client.auth(auth_key))[0]


@router.get('/get', response_model=List[group_schema.GetGroupResponse])
def get_groups(affiliate_id: int = Depends(get_affiliate_id), db: Session = Depends(get_db)):
    return group.get_groups(affiliate_id, db)


@router.get('/{id}', response_model=group_schema.GetGroupResponse)
def get_group_by_id(id: int, db: Session = Depends(get_db), affiliate_id: int = Depends(get_affiliate_id)):
    return group.get_group_by_id(id, affiliate_id, db)


@router.post('/', response_model=group_schema.CreateGroupResponse)
def create_group(
        request: group_schema.GroupCreateRequest,
        db: Session = Depends(get_db),
        affiliate_id: int = Depends(get_affiliate_id)
):
    parsed_phones = phones_parser.parse_phones(request.phones)
    valid_phones = parsed_phones.get('valid')
    valid_phones_count = len(valid_phones)

    response = group_schema.CreateGroupResponse(
        count=valid_phones_count,
        invalid=parsed_phones.get('invalid'),
        result=STATUS_FAILED
    )

    if valid_phones_count:
        group_id = group.create_group(db, request.name, affiliate_id)
        phone.create_phone(db, valid_phones, group_id)
        response.result = STATUS_CREATED
        response.group_id = group_id

    return response


@router.post('/named', response_model=group_schema.CreateGroupResponse)
def create_named_group(
        request: group_schema.NamedGroupCreateRequest,
        db: Session = Depends(get_db),
        affiliate_id: int = Depends(get_affiliate_id)
):
    parsed_phones = phones_parser.parse_phones_with_names(request.phones)
    valid_phones = parsed_phones.get('valid')
    valid_phones_count = len(valid_phones)

    response = group_schema.CreateGroupResponse(
        result=STATUS_FAILED,
        count=len(parsed_phones.get('valid')),
        invalid=parsed_phones.get('invalid')
    )

    if valid_phones_count:
        group_id = group.create_named_group(db, request, affiliate_id)
        phone.create_phone_with_name(db, valid_phones, group_id)
        response.group_id = group_id
        response.result = STATUS_CREATED

    return response


@router.post('/by_file', response_model=group_schema.CreateGroupResponse)
def create_from_file(
        name: str, file: UploadFile,
        db: Session = Depends(get_db),
        affiliate_id: int = Depends(get_affiliate_id)
):
    phones_list = phones_parser.parse_phones_file(file.file)
    valid_phones = phones_list.get('valid')
    valid_phones_count = len(valid_phones)

    response = group_schema.CreateGroupResponse(
        result=STATUS_FAILED,
        invalid=phones_list.get('invalid'),
        count=len(phones_list.get('valid'))
    )

    if valid_phones_count:
        group_id = group.create_group(db, name, affiliate_id)
        phone.create_phone(db, valid_phones, group_id)
        response.result = STATUS_CREATED
        response.group_id = group_id

    return response


@router.post('/named_by_file', response_model=group_schema.CreateGroupResponse)
def create_named_from_file(
        name: str, file: UploadFile,
        db: Session = Depends(get_db),
        affiliate_id: int = Depends(get_affiliate_id)
):
    phones_list = phones_parser.parse_phones_with_name(file.file)
    valid_phones = phones_list.get('valid')
    valid_phones_count = len(valid_phones)

    response = group_schema.CreateGroupResponse(
        result=STATUS_FAILED,
        invalid=phones_list.get('invalid'),
        count=valid_phones_count
    )

    if valid_phones_count:
        group_id = group.create_group(db, name, affiliate_id)
        phone.create_phone_with_name(db, valid_phones, group_id)
        response.result = STATUS_CREATED
        response.group_id = group_id

    return response
