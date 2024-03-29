from pydantic import BaseSettings, Field
import os


class Settings(BaseSettings):
    app_db_url: str = Field(str, env='APP_DB_URL')
    internal_api_role: str = Field(str, env='INTERNAL_API_ROLE')
    internal_api_token: str = Field(str, env='INTERNAL_API_TOKEN')
    internal_api_url: str = Field(str, env='INTERNAL_API_URL')
    country_phone_code: str = Field(str, env='COUNTRY_PHONE_CODE')
    internal_auth_key: str = Field(None, env='INTERNAL_AUTH_KEY')
    sms_cost: float = Field(float, env='SMS_COST')

    class Config:
        env_file = f'{os.path.dirname(os.path.abspath(__file__))}/{os.getenv("ENV_FILE")}'


settings = Settings()
