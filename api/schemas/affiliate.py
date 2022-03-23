from pydantic import BaseModel


class AuthData(BaseModel):
    auth_key: str
    affiliate_id: int
