from fastapi import Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from sqlalchemy import select
from datetime import timedelta, datetime

from errors import InvalidCredentials
from .models import User
from db_config import get_db
from config import Config
from .schemas import *
from .utils import JWTAuth
from .dependencies import *
import os
import shutil
# from main import IMAGES_DIR

REFRESH_TOKEN_EXPIRY = Config.JWT_REFRESH_TOKEN_EXPIRE_DAYS
IMAGES_DIR = "images"


class UserService:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.jwt_auth = JWTAuth()
        self.db = db

    async def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_current_user(self, 
    token_details: dict = Depends(AccessTokenBearer()),
):
        try:
    
            user_email = token_details["user"]["email"]
            user = await self.get_user_by_email(user_email)
            return user
        except:
            raise InvalidToken()


    async def login(self, login_data: LoginRequest):
        email = login_data.email
        password = login_data.password

        user = await self.get_user_by_email(email)

        if user is not None:
            password_valid = await self.jwt_auth.verify_password(password, user.hashed_password)

            if password_valid:
                access_token = await self.jwt_auth.create_token(
                    user_data={
                        "email": user.email,
                        "id": str(user.id),
                    }
                )

                refresh_token = await self.jwt_auth.create_token(
                    user_data={"email": user.email, "id": str(user.id)},
                    refresh=True,
                )

                return JSONResponse(
                    content={
                        "message": "Login successful",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": {"email": user.email, "id": str(user.id)},
                    }
                )

        raise InvalidCredentials()

    async def get_new_access_token(self, token_details: dict = Depends(RefreshTokenBearer())):
        try:
            expiry_timestamp = token_details["exp"]

            if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
                new_access_token = await self.jwt_auth.create_token(user_data=token_details["user"])

                return JSONResponse(content={"access_token": new_access_token})

            raise InvalidToken()
        except:
            raise InvalidToken()

    async def save_profile_picture(self, file: UploadFile) -> str:
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        path = os.path.join(IMAGES_DIR, filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return f"/images/{filename}"
    
    async def get_user(self, user:User):
        return user
    
    async def update_user(self, user: User, payload: UserUpdate):
        if payload.first_name is not None:
            user.first_name = payload.first_name
        if payload.last_name is not None:
            user.last_name = payload.last_name
        if payload.profile_picture is not None:
            user.profile_picture = payload.profile_picture

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token_details: dict = Depends(AccessTokenBearer()),
):
    user_service = UserService(db)
    return await user_service.get_current_user(token_details)