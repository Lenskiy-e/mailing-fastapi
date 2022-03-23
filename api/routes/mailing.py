from fastapi import APIRouter, Depends
from api.schemas import mailing as mailing_schema, affiliate as affiliate_schema
from db.database import get_db
from sqlalchemy.orm import Session
from services import mailing as mailing_service, internal_client as internal_client_service
from repositories import mailing as mailing_repository

router = APIRouter(
    prefix='/mailing',
    tags=['group']
)


@router.post('', response_model=mailing_schema.CreatedMailingResponse, status_code=201)
async def create(
        request: mailing_schema.CreateRequest,
        auth_data: affiliate_schema.AuthData = Depends(internal_client_service.get_affiliate_auth_data),
        db: Session = Depends(get_db)
):
    mailing_data = await mailing_service.create_mailing(request, db, auth_data)

    return mailing_schema.CreatedMailingResponse(
        id=mailing_repository.create(mailing_data, db)
    )
