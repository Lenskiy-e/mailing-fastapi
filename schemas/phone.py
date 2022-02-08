from pydantic import BaseModel


class PhoneWithNameCreateRequest(BaseModel):
    name: str
    phone: str
