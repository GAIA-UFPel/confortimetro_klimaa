from passlib.context import CryptContext
from fastapi_user_auth.auth import Auth
from fastapi_user_auth.auth.backends.db import DbTokenStore

from config.app import get_settings
from app.database import get_session

auth = Auth(
    db=get_session(),
    token_store=DbTokenStore(db=get_session())
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)