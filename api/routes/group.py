import asyncio
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, Header
from api.schemas import group as group_schema, phone as phone_schema
from sqlalchemy.orm import Session
from db.database import get_db
from repositories import group as group_repository, phone
from services import phones_parser, internal_client
from models.group import Group as group_model
from exceptions import group as group_exceptions

STATUS_CREATED = 'Crated'
STATUS_FAILED = 'Failed'
STATUS_UPDATED = 'Updated'

router = APIRouter(
    prefix='/group',
    tags=['group']
)


def get_affiliate_id(auth_key: Optional[str] = Header(None)):
    return asyncio.run(internal_client.auth(auth_key))[0]


@router.get('/get', response_model=List[group_schema.GetGroupResponse])
def get_groups(affiliate_id: int = Depends(get_affiliate_id), db: Session = Depends(get_db)):
    return group_repository.get_groups(affiliate_id, db)


@router.get('/{id}', response_model=group_schema.GetGroupResponse)
def get_group_by_id(id: int, db: Session = Depends(get_db), affiliate_id: int = Depends(get_affiliate_id)):
    group = group_repository.get_group_by_id(id, db)

    if not group.has_affiliate(affiliate_id):
        raise group_exceptions.GroupBelongsToAffiliateException(group.id, affiliate_id)

    return group


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
        group_id = group_repository.create_group(db, request.name, affiliate_id)
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
        group_id = group_repository.create_named_group(db, request, affiliate_id)
        phone.create_phone_with_name(db, valid_phones, group_id)
        response.group_id = group_id
        response.result = STATUS_CREATED

    return response


@router.patch('/{id}', response_model=group_schema.CreateGroupResponse)
def update_group(
        group_id: int,
        request: group_schema.GroupCreateRequest,
        db: Session = Depends(get_db),
        affiliate_id: int = Depends(get_affiliate_id)
):
    parsed_phones = phones_parser.parse_phones(request.phones)
    valid_phones = parsed_phones.get('valid')
    valid_phones_count = len(valid_phones)
    group = group_repository.get_group_instance_by_id(group_id, db)
    update_group_name(group, affiliate_id, request.name, db).first()

    response = group_schema.CreateGroupResponse(
        count=valid_phones_count,
        invalid=parsed_phones.get('invalid'),
        result=STATUS_UPDATED
    )

    if valid_phones_count:
        phone.create_phone(db, valid_phones, group_id)
        response.group_id = group_id

    return response


@router.patch('/{id}/named', response_model=group_schema.CreateGroupResponse)
def update_named_group(
        group_id: int,
        request: group_schema.NamedGroupCreateRequest,
        db: Session = Depends(get_db),
        affiliate_id: int = Depends(get_affiliate_id)
):
    parsed_phones = phones_parser.parse_phones_with_names(request.phones)
    valid_phones = parsed_phones.get('valid')
    valid_phones_count = len(valid_phones)
    group = group_repository.get_group_instance_by_id(group_id, db)

    if not group.first().is_named:
        raise group_exceptions.GroupIsNotNamed(group_id)

    response = group_schema.CreateGroupResponse(
        count=valid_phones_count,
        invalid=parsed_phones.get('invalid'),
        result=STATUS_UPDATED
    )

    update_group_name(group, affiliate_id, request.name, db)
    if valid_phones_count:
        phone.create_phone_with_name(db, valid_phones, group_id)
        response.group_id = group_id

    return response


@router.post('/parse_file', response_model=phone_schema.ParsedPhonesResponse)
def parse_from_file(file: UploadFile):
    return phones_parser.parse_phones_file(file.file)


@router.post('/parse_named_file', response_model=phone_schema.ParsedNamedPhonesResponse)
def parse_from_named_file(file: UploadFile):
    return phones_parser.parse_phones_with_name_file(file.file)


def update_group_name(group: group_model, affiliate_id: int, name: str, db: Session) -> group_model:
    if not group.first().has_affiliate(affiliate_id):
        raise group_exceptions.GroupBelongsToAffiliateException(group.id, affiliate_id)

    group_repository.update_name(group, db, name)

    return group
