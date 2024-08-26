from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_user_auth.admin.site import AuthAdminSite

from app.database import get_session
from app.routes.api import router as api_router
from app.utils.auth import auth

app = FastAPI()

site = AuthAdminSite(
    settings=Settings(),
    db=get_session(),
    auth=auth
)
site.mount_app(app)

app.include_router(api_router)