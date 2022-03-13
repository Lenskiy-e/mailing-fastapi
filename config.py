from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    app_db_url: str
    internal_api_role: str
    internal_api_token: str
    internal_api_url: str
    country_phone_code: str

    class Config:
        env_file = os.getenv('ENV_FILE')


settings = Settings()
