import uuid
from datetime import datetime, timedelta

from fastapi import Response, status, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User, ConfirmationToken
from app.request_forms import LoginRequest, RegisterRequest
from app.utils.auth import authenticate_active_user, create_access_token

class AuthController:
    @classmethod
    async def login(cls,
                    req: LoginRequest,
                    session: AsyncSession):
        """
        Login existing user and send back a JWK authentication token.
        """
        user = await authenticate_active_user(req.email, req.password, session)
        jwt_token = create_access_token(
            {
                "email": user.email
            }
        )

        return Response(headers={
                "Authorization": f"Bearer {jwt_token}"
            })
    
    @classmethod
    async def register(cls,
                       req: RegisterRequest,
                       session: AsyncSession):
        user = (await session.exec(select(User).where(User.username == req.username))).first()
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use")

        # Create the new user
        new_user = User(
            username = req.username,
            email = req.email,
            password = get_password_hash(req.password),
            create_date = datetime.now(),
            is_admin = req.is_admin,
            is_active = req.is_active,
            has_write_access = req.has_write_access or req.is_admin
        )

        new_confirmation_token = ConfirmationToken(
            token = str(uuid.uuid4()),
            date_expiration = datetime.now() + timedelta(hours=EMAIL_CONFIRMATION_EXPIRE_HOURS),
            email = req.email
        )

        session.add(new_user)
        session.add(new_confirmation_token)
        await session.commit()

        return Response(status_code=status.HTTP_200_OK)
    
    @classmethod
    async def confirm_email(cls, 
                            token: str, 
                            user: User, 
                            session: AsyncSession):
        confirmation_token = (await session.exec(select(ConfirmationToken).where(ConfirmationToken.id == token))).first()
        if not confirmation_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        
        if confirmation_token.expiration < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
        
        user = confirmation_token.user
        user.is_active = True

        await session.delete(confirmation_token)
        await session.commit()

        return Response(status_code=status.HTTP_200_OK)