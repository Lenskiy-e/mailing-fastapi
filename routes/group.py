from fastapi import APIRouter, Depends, UploadFile
from schemas import group as group_schema
from sqlalchemy.orm import Session
from db.database import get_db
from repositories import group, phone
from services.phones_file_parser import parse_phones_file, parse_phones_with_name

router = APIRouter(
    prefix='/group',
    tags=['group']
)


@router.post('/', response_model=group_schema.CreateGroupResponse)
def create_group(request: group_schema.GroupCreateRequest, db: Session = Depends(get_db)):
    group_id = group.create_group(db, request.name)
    phone.create_phone(db, request.phones, group_id)

    return group_schema.CreateGroupResponse(
        result='Created',
        group_id=group_id
    )


@router.post('/named', response_model=group_schema.CreateGroupResponse)
def create_named_group(request: group_schema.NamedGroupCreateRequest, db: Session = Depends(get_db)):
    group_id = group.create_named_group(db, request)
    phone.create_phone_with_name(db, request.phones, group_id)

    return group_schema.CreateGroupResponse(
        result='Created',
        group_id=group_id
    )


@router.post('/by_file', response_model=group_schema.CreateGroupByFileResponse)
def create_from_file(name: str, file: UploadFile, db: Session = Depends(get_db)):
    group_id = group.create_group(db, name)
    phones_list = parse_phones_file(file.file)
    phone.create_phone(db, phones_list.get('valid'), group_id)

    return group_schema.CreateGroupByFileResponse(
        result='created',
        group_id=group_id,
        invalid=phones_list.get('invalid')
    )


@router.post('/named_by_file', response_model=group_schema.CreateNamedGroupByFileResponse)
async def create_named_from_file(name: str, file: UploadFile, db: Session = Depends(get_db)):
    group_id = group.create_group(db, name)
    phones_list = await parse_phones_with_name(file)
    phone.create_phone_with_name(db, phones_list.get('valid'), group_id)

    return group_schema.CreateGroupByFileResponse(
            result='created',
            group_id=group_id,
            invalid=phones_list.get('invalid')
        )
