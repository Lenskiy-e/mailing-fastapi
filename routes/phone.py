from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from repositories import phone

router = APIRouter(
    prefix='/phone',
    tags=['phone']
)


@router.delete('/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    phone.delete(db, id)

    return {
        'result': 'deleted'
    }