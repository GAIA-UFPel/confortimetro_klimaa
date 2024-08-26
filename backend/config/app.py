from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Klimaa API"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    db_url: str = "database/database.sqlite"
    host: str = '127.0.0.1'
    port: int = 8000
    email_host: str
    email_port: int
    email_host_user: str
    email_host_password: str
    email_confirmation_expire_hours: int

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

@lru_cache
def get_settings():
    return Settings()